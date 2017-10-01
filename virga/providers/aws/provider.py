import uuid

from multiprocessing import Manager, Process
import os
import boto3

import jmespath

from botocore.exceptions import ParamValidationError, ClientError

from virga import VirgaException
from virga.providers import AbstractProvider
from virga.providers.aws.vismaclient import VismaClient


class Provider(AbstractProvider):
    """Implementation of AWS provider class."""

    def __init__(self, config: dict, args: any):  # NOQA
        super(Provider, self).__init__(config, args)
        self.required_params = [
            'region_name',
        ]
        self.params = config['provider'].get('params', {})
        self.role = {}
        self.definition_file = os.path.join(os.path.dirname(__file__), 'aws.yaml')

    def assume_role(self):
        """Generate temporary credentials with STS assume role."""
        try:
            role_arn = self.config['provider']['extra']['role_arn']
            sts = boto3.client('sts')
            response = sts.assume_role(RoleArn=role_arn, RoleSessionName=str(uuid.uuid4()))
            self.role['aws_access_key_id'] = response['Credentials']['AccessKeyId']
            self.role['aws_secret_access_key'] = response['Credentials']['SecretAccessKey']
            self.role['aws_session_token'] = response['Credentials']['SessionToken']
        except KeyError:
            self.logger.debug('Role ARN not set')
        except ParamValidationError:
            raise VirgaException('Role ARN not valid')
        except ClientError as exc:
            raise VirgaException('Assume role client exception: %s' % str(exc))

    def process(self, resource_section: str, resource_object: dict, shared_messages: list) -> Process:
        """
        Start and return the process.

        This method is made for facilitating the tests.

        :param resource_section: Section of the resource to evaluate
        :param resource_object: Object to evaluate
        :param shared_messages: Shared messages managed list
        :return: The process instantiated
        """
        resource_definition = self.definition[resource_section]
        process = Process(target=self.evaluate, args=(resource_object, resource_definition, shared_messages))
        process.start()
        return process

    def launch_tests(self):
        """
        Launch the battery of tests.

        Requests are sent using the `request` method which starts a separated process.
        When the processes are all concluded, the outcome is logged.
        """
        jobs = []

        with Manager() as manager:
            shared_messages = manager.list()
            for resource_section, resource_objects in self.config.get('tests', {}).items():
                for resource_object in resource_objects:
                    process = self.process(resource_section, resource_object, shared_messages)
                    jobs.append(process)

            for job in jobs:
                job.join()

            self.logs(shared_messages)
            self.result(shared_messages)

    def client(self, resource_definition: dict, resource_object: dict) -> dict:
        """
        Entry-point for calling a client.

        If the client is virga searches for the custom method.
        If the client is NOT virga searches for the boto3 definition.

        :param resource_definition: Section definition
        :param resource_object: Object filter
        :return: Response from AWS
        """
        if resource_definition['client'] == 'virga':
            client = VismaClient(self.params, self.role)
            return getattr(client, resource_definition['action'])(resource_definition, resource_object)
        else:
            client = boto3.client(resource_definition['client'], **self.params, **self.role)
            filters = self.format_filters(resource_definition, resource_object)
            return getattr(client, resource_definition['action'])(Filters=filters)

    def evaluate(self, resource_object: dict, resource_definition: dict, shared_messages: list):
        """
        Get the resource information and execute the tests.

        :param resource_object: Resource to analyse
        :param resource_definition: Resource definition
        :param shared_messages: List of shared messages
        """
        response = self.client(resource_definition, resource_object)
        items = self.flatten_items(response, resource_definition['prefix'])
        for resource in items:
            resource_id = resource[resource_definition['resource_id']]
            for test in resource_object['assertions']:
                outcome = self.assertion(test, resource_definition['context'], resource, resource_id)
                shared_messages.append(outcome)

    def action(self):
        """Entry point of the launch for the Provider."""
        self.assume_role()
        self.launch_tests()

    @staticmethod
    def format_filters(definition: dict, test: dict) -> list:
        """
        Format the filter for query the resources.

        :param definition: Resource definition
        :param test:
        """
        try:
            filter_key = [x for x in definition['identifiers'].keys() if x in test.keys()][0]
            return [{
                'Name': definition['identifiers'][filter_key], 'Values': [test[filter_key]]
            }]
        except (KeyError, IndexError):
            raise VirgaException('Invalid configuration')

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
            resource_definition = self.definition[section]
            response = self.client(resource_definition, {identifier: resource_id})
            items = self.flatten_items(response, resource_definition['prefix'])
            return items[0][resource_definition['resource_id']]
        except (KeyError, IndexError):
            raise VirgaException('Lookup %s %s %s failed' % (section, identifier, resource_id))
