from unittest import TestCase
from unittest.mock import patch, call

from tests import MockArgParse, fixture
from virga.common import VirgaException
from virga.providers.aws import Provider
from virga.providers.aws.virgaclient import VirgaClient


@patch('botocore.client.BaseClient._make_api_call')
class TestAWS(TestCase):
    def setUp(self):
        self.arg_parse = MockArgParse(
            debug=False, silent=True, logfile=None, output='/tmp', definitions=None
        )
        self.provider = Provider(self.arg_parse)

    def test_lookup_success(self, mock_call):
        mock_call.return_value = fixture('subnet.json', get_json=True)
        resource_id = self.provider.lookup('subnets', 'name', 'my-subnet')
        self.assertEqual('subnet-0123456789', resource_id)

    def test_lookup_failure(self, mock_call):
        mock_call.return_value = fixture('empty-subnet.json', get_json=True)
        self.assertEqual('Lookup subnets name no-subnet failed', self.provider.lookup('subnets', 'name', 'no-subnet'))

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
        self.provider.evaluate(test, self.provider.definitions['subnets'], [])
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

    @patch('virga.providers.abstract.AbstractProvider.assertion')
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
        self.provider.tests = fixture('tests.yaml', get_yaml=True)
        self.provider.action()
        self.assertEqual(3, mock_process.call_count)

    @patch('virga.providers.aws.Provider.read_definitions')
    def test_sample_invokes_read_definition(self, mock_read_definition, *args):
        mock_read_definition.return_value = fixture('valid-definition.yaml', get_yaml=True)
        self.provider.sample('subnets', 'subnet-123456')
        mock_read_definition.assert_called_once_with()

    def test_convert_struct(self, *args):
        resource = {
            'ImageId': 'ami-01234567890',
            'IsReal': True,
            'HowMany': 200
        }
        expected = [
            "ImageId=='ami-01234567890'",
            'IsReal==`true`',
            'HowMany==`200`',
        ]
        self.assertListEqual(expected, self.provider.convert_struct(resource))

    def test_convert_struct_dict(self, *args):
        resource = {
            'Placement': {
                'AZ': 'eu-west-2a',
                'GroupName': False,
                'Tenancy': 1
            }
        }
        expected = [
            "Placement.AZ=='eu-west-2a' && Placement.GroupName==`false` && Placement.Tenancy==`1`"
        ]
        self.assertListEqual(expected, self.provider.convert_struct(resource))

    def test_convert_struct_list_simple(self, *args):
        resource = {
            'Data': [
                'Data 1',
                True,
                3
            ]
        }
        expected = [
            "Data[]==['Data 1', `true`, `3`]"
        ]
        self.assertListEqual(expected, self.provider.convert_struct(resource))

    def test_convert_struct_list_dicts(self, *args):
        resource = {
            'Tags': [
                {'Key': 'Name', 'Value': 'Test tag'},
                {'Key': 'Env', 'Value': 'dev'},
                {'Key': 'Num', 'Value': 1},
                {'Key': 'Valid', 'Value': False},
            ]
        }
        expected = [
            "Tags[?Key=='Name' && Value=='Test tag']",
            "Tags[?Key=='Env' && Value=='dev']",
            "Tags[?Key=='Num' && Value==`1`]",
            "Tags[?Key=='Valid' && Value==`false`]",
        ]
        self.assertListEqual(expected, self.provider.convert_struct(resource))

    @patch('virga.providers.aws.Provider.read_definitions')
    def test_sample_definition_not_found(self, mock_read_definition, *args):
        mock_read_definition.return_value = fixture('valid-definition.yaml', get_yaml=True)
        with self.assertRaisesRegex(VirgaException, 'Resource definition not found'):
            self.provider.sample('not_here', 'id-123456')

    @patch('virga.providers.aws.Provider.read_definitions')
    def test_sample_definition_is_virga_client(self, mock_read_definition, *args):
        mock_read_definition.return_value = fixture('valid-definition.yaml', get_yaml=True)
        with self.assertRaisesRegex(VirgaException, 'Resource sample for certificates not supported'):
            self.provider.sample('certificates', 'id-123456')

    @patch('virga.providers.aws.Provider.flatten_items')
    @patch('virga.providers.aws.Provider.read_definitions')
    def test_sample_resource_not_found(self, mock_read_definition, mock_flatten_items, *args):
        mock_read_definition.return_value = fixture('valid-definition.yaml', get_yaml=True)
        mock_flatten_items.return_value = []
        with self.assertRaisesRegex(VirgaException, 'Resource not found'):
            self.provider.sample('subnets', 'id-123456')

    def test_find_certificate_no_certificates_found(self, mock_call):
        mock_call.side_effect = [{}, {}]
        with self.assertRaisesRegex(VirgaException, 'Lookup certificates domain_name any-domain.it failed'):
            VirgaClient.find_certificate({}, {'domain_name': 'any-domain.it'})

    def test_find_certificate_no_domain_found(self, mock_call):
        mock_call.side_effect = [{'CertificateSummaryList': [{'DomainName': 'any-domain.it'}]}, IndexError()]
        with self.assertRaisesRegex(VirgaException, 'Lookup certificates domain_name any-domain.it failed'):
            VirgaClient.find_certificate({}, {'domain_name': 'any-domain.it'})
