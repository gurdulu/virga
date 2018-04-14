from unittest import TestCase
from unittest.mock import patch

from tests import fixture
from tests.fixtures import responses
from virga.providers.aws.virgaclient import VirgaClient


@patch('botocore.client.BaseClient._make_api_call')
class TestVirgaClient(TestCase):

    def test_find_certificate_expected_bahaviour(self, mock_call):
        mock_call.side_effect = [
            responses.acm_certificate_list,
            fixture('certificate.json', get_json=True)
        ]
        expected = responses.acm_result_find_certificate
        self.assertDictEqual(expected, VirgaClient.find_certificate({'domain_name': 'my.any-domain.com'}))

    def test_find_certificate_domain_not_found(self, mock_list_certificates):
        mock_list_certificates.return_value = {'CertificateSummaryList': []}
        self.assertIsNone(VirgaClient.find_certificate({'domain_name': 'my.any-domain.com'}))

    def test_find_elbv2_call_sequence(self, mock_call):
        mock_call.side_effect = [
            responses.elbv2_describe_load_balancers,
            responses.elbv2_describe_load_balancer_attributes,
            responses.elbv2_describe_listeners,
            responses.elbv2_describe_target_groups,
            responses.elbv2_describe_target_group_attributes,
            responses.elbv2_describe_tags,
        ]
        expected = responses.elbv2_result
        self.assertDictEqual(expected, VirgaClient.find_elbv2({'name': 'my-elbv2'}))

    def test_find_elbv2_index_error(self, mock_call):
        mock_call.side_effect = IndexError()
        self.assertIsNone(VirgaClient.find_elbv2({'name': 'my-elbv2'}))

    def test_find_elbv2_key_error(self, mock_call):
        mock_call.side_effect = KeyError()
        self.assertIsNone(VirgaClient.find_elbv2({'name': 'my-elbv2'}))

    def test_find_elb_call_sequence(self, mock_call):
        self.maxDiff = None
        mock_call.side_effect = [
            responses.elb_describe_load_balancers,
            responses.elb_describe_tags,
        ]
        expected = responses.elb_result
        self.assertDictEqual(expected, VirgaClient.find_elb({'name': 'my-elb'}))

    def test_find_elb_index_error(self, mock_call):
        mock_call.side_effect = IndexError()
        self.assertIsNone(VirgaClient.find_elb({'name': 'my-elb'}))

    def test_find_elb_key_error(self, mock_call):
        mock_call.side_effect = KeyError()
        self.assertIsNone(VirgaClient.find_elb({'name': 'my-elb'}))
