from unittest import TestCase
from unittest.mock import patch, call

from tests import MockArgParse, fixture
from virga.exceptions import VirgaException
from virga.providers.aws import Provider


@patch('botocore.client.BaseClient._make_api_call')
class TestAWS(TestCase):
    def setUp(self):
        self.arg_parse = MockArgParse(
            debug=False, silent=True, logfile=None, output='/tmp', definition=None
        )
        self.provider = Provider({'provider': {}}, self.arg_parse)
        self.valid_credentials = {
            'Credentials': {
                'AccessKeyId': 'access_key_id',
                'SecretAccessKey': 'secret_access_key',
                'SessionToken': 'session_token',
            }
        }

    def test_lookup_success(self, mock_call):
        mock_call.return_value = fixture('subnet.json', get_json=True)
        resource_id = self.provider.lookup('subnets', 'name', 'my-subnet')
        self.assertEqual('subnet-0123456789', resource_id)

    def test_lookup_failure(self, mock_call):
        mock_call.return_value = fixture('empty-subnet.json', get_json=True)
        with self.assertRaisesRegex(VirgaException, 'Lookup subnets name no-subnet failed'):
            self.provider.lookup('subnets', 'name', 'no-subnet')

    def test_flatten_items(self, *args):
        response = fixture('reservations-instances.json', get_json=True)
        result = self.provider.flatten_items(response, 'Reservations.Instances')
        expected = fixture('only-instances.json', get_json=True)
        self.assertListEqual(expected, result)

    def test_format_filters(self, *args):
        definition = {'identifiers': {'id': 'resource-id', 'name': 'tag:Name'}}
        test = {'name': 'resource-name'}
        expected = [{'Name': 'tag:Name', 'Values': ['resource-name']}]
        self.assertListEqual(expected, self.provider.format_filters(definition, test))

    def test_format_filters_invalid_configuration(self, *args):
        definition = {'identifiers': {'id': 'resource-id', 'name': 'tag:Name'}}
        test = {'another-key': 'resource-name'}
        with self.assertRaisesRegex(VirgaException, 'Invalid configuration'):
            self.provider.format_filters(definition, test)

    def test_evaluate_no_assertions_calls_aws(self, mock_call):
        test = {
            'name': 'my-subnet',
            'assertions': []
        }
        expected = 'DescribeSubnets', {
            'Filters': [{'Name': 'tag:Name', 'Values': ['my-subnet']}]
        }
        self.provider.evaluate(test, self.provider.definition['subnets'], [])
        mock_call.assert_called_once_with(*expected)

    @patch('virga.providers.aws.Provider.format_filters')
    def test_evaluate_no_assertions_calls_format_filters(self, mock_format_filters, *args):
        test = {
            'name': 'my-subnet',
            'assertions': []
        }
        definition = {
            'client': 'ec2',
            'action': 'describe_subnets',
            'context': 'Subnets',
            'prefix': 'Subnets',
            'resource_id': 'SubnetId',
            'identifiers': {
                'id': 'subnet-id',
                'name': 'tag:Name'
            }
        }
        self.provider.evaluate(test, definition, [])
        mock_format_filters.assert_called_once_with(definition, {'name': 'my-subnet', 'assertions': []})

    @patch('virga.providers.AbstractProvider.assertion')
    def test_evaluate_no_assertions_calls_assertion(self, mock_assertion, mock_call):
        mock_call.return_value = fixture('subnet.json', get_json=True)
        test = {
            'name': 'my-subnet',
            'assertions': [
                "AvailabilityZone=='eu-west-2a'",
                "CidrBlock=='10.0.0.0/24'",
            ]
        }
        definition = {
            'client': 'ec2',
            'action': 'describe_subnets',
            'context': 'Subnets',
            'prefix': 'Subnets',
            'resource_id': 'SubnetId',
            'identifiers': {
                'id': 'subnet-id',
                'name': 'tag:Name'
            }
        }

        self.provider.evaluate(test, definition, [])

        subnet_data = {
            'AvailabilityZone': 'eu-west-2a',
            'AvailableIpAddressCount': 248,
            'CidrBlock': '10.0.0.0/24',
            'DefaultForAz': False,
            'MapPublicIpOnLaunch': True,
            'State': 'available',
            'SubnetId': 'subnet-0123456789',
            'VpcId': 'vpc-0123456789',
            'AssignIpv6AddressOnCreation': False,
            'Ipv6CidrBlockAssociationSet': [],
            'Tags': [
                {'Key': 'environment', 'Value': 'staging'},
                {'Key': 'Name', 'Value': 'my-subnet'}
            ]
        }
        expected = [
            call("AvailabilityZone=='eu-west-2a'", 'Subnets', subnet_data, 'subnet-0123456789'),
            call("CidrBlock=='10.0.0.0/24'", 'Subnets', subnet_data, 'subnet-0123456789')
        ]
        mock_assertion.assert_has_calls(expected, any_order=True)

    @patch('virga.providers.aws.Provider.process')
    def test_launch_tests(self, mock_process, *args):
        self.provider.config = fixture('config.yaml', get_yaml=True)
        self.provider.action()
        self.assertEqual(3, mock_process.call_count)
