from unittest import TestCase
from unittest.mock import patch

from tests import MockArgParse
from virga import VirgaException, get_provider_class


class TestCommon(TestCase):

    @patch('virga.assert_parser')
    def test_not_existing_provider_name_raise_virga_exc(self, mock_parser):
        with self.assertRaisesRegex(VirgaException, 'Provider module not found'):
            get_provider_class(MockArgParse(provider=''))

    @patch('virga.assert_parser')
    def test_invalid_module_raise_virga_exc(self, mock_parser):
        with self.assertRaisesRegex(VirgaException, 'Provider module not found'):
            get_provider_class(MockArgParse(provider='no_module'))

    def test_invalid_class_raise_virga_exc(self):
        with self.assertRaisesRegex(VirgaException, 'Provider class not found'):
            get_provider_class(MockArgParse())
