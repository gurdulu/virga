from unittest import TestCase
from unittest.mock import patch

from tests import fixture
from tests.fixtures import responses
from virga.common import VirgaException
from virga.providers.aws.virgaclient import VirgaClient


@patch('botocore.client.BaseClient._make_api_call')
class TestVirgaClient(TestCase):

    def test_find_certificate_expected_bahaviour(self, mock_call):
        mock_call.side_effect = [
            responses.acm_certificate_list,
            fixture('certificate.json', get_json=True)
        ]
        VirgaClient.find_certificate({'domain_name': 'my.any-domain.com'})

    def test_find_certificate_domain_not_found(self, mock_list_certificate):
        mock_list_certificate.return_value = {'CertificateSummaryList': []}
        with self.assertRaisesRegex(VirgaException, 'Lookup certificates domain_name my.any-domain.com failed'):
            VirgaClient.find_certificate({'domain_name': 'my.any-domain.com'})
