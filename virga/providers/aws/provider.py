from multiprocessing import Manager
from multiprocessing.pool import Pool
import os

import boto3

import jmespath
import yaml

from virga import VirgaException
from virga.providers.abstract import AbstractProvider
from virga.providers.aws.virgaclient import VirgaClient


class Provider(AbstractProvider):
    """Implementation of AWS provider class."""

    def __init__(self, args: any):  # NOQA
        super(Provider, self).__init__(args)
        self.definitions_path = os.path.join(os.path.dirname(__file__), 'definitions')

    def client(self, definition: dict, test: dict) -> dict:
        """
        Entry-point for calling a client.

        If the client is virga searches for the custom method.
        If the client is NOT virga searches for the boto3 definition.

        :param definition: Section definition
        :param test: Object filter
        :return: Response from AWS
        """
        if definition['client'] == 'virga':
            client = VirgaClient()
            return getattr(client, definition['action'])(test)
        client = boto3.client(definition['client'])
        formatted_filter = self.format_filter(definition, test)
        return getattr(client, definition['action'])(**formatted_filter)

    def evaluate(self, test: dict, definition: dict, shared_messages: list):
        """
        Get the resource information and execute the tests.

        :param test: Test
        :param definition: Resource definition
        :param shared_messages: List of shared messages
        """
        response = self.client(definition, test)
        items = self.flatten_items(response, definition['prefix'])

        # None items are resources not found
        if not items:
            items = [None]
        if any(x is None for x in items):
            identifier = {k: v for k, v in test.items() if k != 'assertions'}
            items = [{definition['resource_id']: '%s = %s (RESOURCE NOT FOUND)' % (
                next(iter(identifier.keys())),
                next(iter(identifier.values())))}]

        for resource in items:
            if isinstance(definition['resource_id'], list):
                resource_id = ' - '.join([resource[x] for x in definition['resource_id']])
            else:
                resource_id = resource[definition['resource_id']]
            for test in test['assertions']:
                outcome = self.assertion(test, definition['context'], resource, resource_id)
                shared_messages.append(outcome)

    def action(self):
        """
        Entry point of the launch for the Provider.

        Launch the battery of tests.
        Requests are sent using the `request` method which starts a separated process.
        When the processes are all concluded, the outcome is logged.
        """

        with Manager() as manager:
            pool_kwargs = {}
            if self.args.processes is not None:
                pool_kwargs['processes'] = self.args.processes
            pool = Pool(**pool_kwargs)

            shared_messages = manager.list()
            error_callback_messages = []

            for test_section, tests in self.tests.items():
                definition = self.definitions[test_section]
                for test in tests:
                    pool.apply_async(
                        self.evaluate, (test, definition, shared_messages),
                        error_callback=lambda x: error_callback_messages.append(x)
                    )
                    if error_callback_messages:
                        break

            pool.close()
            pool.join()

            if error_callback_messages:
                raise VirgaException(error_callback_messages[0])
            self.logs(shared_messages)
            self.result(shared_messages)

    @staticmethod
    def format_filter(definition: dict, test: dict) -> dict:
        """
        Format the filter for query the resources.

        :param definition: Resource definition
        :param test: Test definition
        :return: The filter
        """
        result = {}
        try:
            filter_key = [x for x in definition['identifiers'].keys() if x in test.keys()][0]
            identifier = definition['identifiers'][filter_key]
            if identifier['type'] == 'filter':
                result = {'Filters': [{'Name': identifier['key'], 'Values': [test[filter_key]]}]}
            elif identifier['type'] == 'list':
                result = {identifier['key']: [test[filter_key]]}
            elif identifier['type'] == 'and':
                result = {}
                for key in identifier['key']:
                    result[key] = test[filter_key][key]
            return result
        except (KeyError, IndexError):
            keys = set(test.keys())
            keys.remove('assertions')
            raise VirgaException(f"Invalid resource name '{keys.pop()}'")

    def flatten_items(self, response: dict, prefix: str) -> list:
        """
        Filter the resources extracting the useful information.

        Useful for avoiding noise in the data. The results are flattened.

        :param response: Response from the provider
        :param prefix: Data to filer
        :return:
        """
        return self.flatten(jmespath.search(prefix.replace('.', '[].'), response))

    def lookup(self, section: str, identifier: str, resource_id: str) -> str:
        """
        Lookup function.

        :param section: Section to query
        :param identifier: Identifier to search
        :param resource_id: Resource ID
        :return: The resource selected
        :raises VirgaException: If the resource is not found
        """
        try:
            definition = self.definitions[section]
            response = self.client(definition, {identifier: resource_id})
            items = self.flatten_items(response, definition['prefix'])
            return items[0][definition['resource_id']]
        except (KeyError, IndexError):
            raise VirgaException('Lookup %s %s %s failed' % (section, identifier, resource_id))

    def sample(self, resource_type: str, resource_id: str) -> str:
        """
        Method to invoke for generating a test sample.

        :param resource_type: Type of resource to sample
        :param resource_id: ID of resource to sample
        :return: Test in YAML format
        """
        try:
            definition = self.definitions[resource_type]
        except KeyError:
            raise VirgaException('Resource definition not found')
        if definition['client'] == 'virga':
            raise VirgaException('Resource sample for %s not supported' % resource_type)
        response = self.client(definition, {'id': resource_id})
        try:
            flattened_results = self.flatten_items(response, definition['prefix'])
            result = self.convert_to_test(resource_type, resource_id, flattened_results[0])
        except IndexError:
            raise VirgaException('Resource not found')
        return result

    @staticmethod
    def convert_list_to_test_format(origin: str, data: list) -> str:
        """
        Convert a list in a format ready for tests.

        :param origin: The parent key of the list
        :param data: The list to convert
        :return: The resulting string
        """
        result = []
        for item in data:
            if isinstance(item, str):
                result.append("'%s'" % item)
            elif isinstance(item, bool):
                result.append("`%s`" % 'true' if item else 'false')
            elif isinstance(item, (int, float)):
                result.append("`%s`" % item)
        return '%s[]==[%s]' % (origin, ', '.join(result))

    @staticmethod
    def convert_dicts_to_test_format(origin: str, data: list) -> list:
        """
        Convert a list of dictionaries in a format ready for tests.

        :param origin: The parent key of the dictionary
        :param data: The list of dictionaries to convert
        :return: The resulting assertions
        """
        result = []
        for item in data:
            elements = []
            for k, value in item.items():
                if isinstance(value, str):
                    elements.append("%s=='%s'" % (k, value))
                elif isinstance(value, bool):
                    elements.append("%s==`%s`" % (k, 'true' if value else 'false'))
                elif isinstance(value, (int, float)):
                    elements.append("%s==`%s`" % (k, value))
            result.append('%s[?%s]' % (origin, ' && '.join(elements)))
        return result

    @staticmethod
    def convert_dict_to_test_format(origin: str, data: dict) -> str:
        """
        Convert a dictionary in a format ready for tests.

        :param origin: The parent key of the dictionary
        :param data: The dictionary to convert
        :return: The resulting string
        """
        result = []
        for k, value in data.items():
            if isinstance(value, str):
                result.append("%s.%s=='%s'" % (origin, k, value))
            elif isinstance(value, bool):
                result.append("%s.%s==`%s`" % (origin, k, 'true' if value else 'false'))
            elif isinstance(value, (int, float)):
                result.append("%s.%s==`%s`" % (origin, k, value))
        return " && ".join(result)

    def convert_struct(self, resource: dict) -> list:
        """
        Convert a dictionary in a list of assertions.

        :param resource: Resource to analyse
        :return: List of assertions
        """
        assertions = []
        for k, value in resource.items():
            if isinstance(value, str):
                assertions.append("%s=='%s'" % (k, value))
            elif isinstance(value, bool):
                assertions.append("%s==`%s`" % (k, 'true' if value else 'false'))
            elif isinstance(value, (int, float)):
                assertions.append("%s==`%s`" % (k, value))
            elif isinstance(value, dict):
                assertions.append(self.convert_dict_to_test_format(k, value))
            elif isinstance(value, list) and not all(isinstance(item, dict) for item in value):
                assertions.append(self.convert_list_to_test_format(k, value))
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                assertions += self.convert_dicts_to_test_format(k, value)
        return assertions

    def convert_to_test(self, resource_type: str, resource_id: str, resource: dict) -> str:
        """
        Convert the resource object into a list of assertions.

        :param resource_type: Type of resource
        :param resource_id: Resource ID
        :param resource: Resource object
        :return: The sample string in YAML format
        """
        assertions = self.convert_struct(resource)
        result = {resource_type: [{'id': resource_id, 'assertions': assertions}]}
        return yaml.dump(result, default_flow_style=False)
