from unittest import TestCase

import os

import sys
from unittest.mock import patch

from tests import fixtures, MockArgParse, MockProvider

# https://stackoverflow.com/questions/8658043/how-to-mock-an-import

sys.modules['virga.providers.provider_not_there'] = __import__('unittest.mock')

from virga import virga  # NOQA
from virga.asserts import parser  # NOQA
from virga.exceptions import VirgaException  # NOQA


class TestVirgaAsserts(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('config', help='Test configuration file')
        mock_add_argument.assert_any_call('-definition', help='Definition file')
        mock_add_argument.assert_any_call('-logfile', help='Log file')
        mock_add_argument.assert_any_call('-debug', help='Show debug', action='store_true', default=False)
        mock_add_argument.assert_any_call('-silent', help='Do not output results', action='store_true', default=False)
        mock_add_argument.assert_any_call('-output', help='Resource output directory')
        mock_parse_args.assert_called_once()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_config')
    @patch('virga.asserts.get_provider_class')
    def test_virga_function_invoke_parser_and_read_config(self, mock_get_provider_class, mock_read_config, mock_parser):
        mock_read_config.return_value = {'provider': 'aws'}
        virga()
        mock_parser.assert_called_once_with()
        mock_read_config.assert_called_once()
        mock_get_provider_class.assert_called_once()

    @patch('virga.asserts.parser')
    def test_not_existing_configuration_file_raise_virga_exc(self, mock_parser):
        mock_parser.return_value = MockArgParse(config='file-not-here.yaml')
        with self.assertRaisesRegex(VirgaException, 'Configuration file not found'):
            virga()

    @patch('virga.asserts.parser')
    def test_invalid_configuration_file_raise_virga_exc(self, mock_parser):
        mock_parser.return_value = MockArgParse(config=os.path.join(fixtures, 'invalid.yaml'))
        with self.assertRaisesRegex(VirgaException, 'Invalid configuration file'):
            virga()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_config')
    def test_not_existing_provider_name_raise_virga_exc(self, mock_read_config, mock_parser):
        mock_parser.return_value = MockArgParse(config=None)
        mock_read_config.return_value = {'provider': None}
        with self.assertRaisesRegex(VirgaException, 'Provider missing'):
            virga()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_config')
    def test_invalid_module_raise_virga_exc(self, mock_read_config, mock_parser):
        mock_parser.return_value = MockArgParse(config=None)
        mock_read_config.return_value = {'provider': {'name': 'module_not_there'}}
        with self.assertRaisesRegex(VirgaException, 'Provider module not found'):
            virga()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_config')
    def test_invalid_class_raise_virga_exc(self, mock_read_config, mock_parser):
        mock_parser.return_value = MockArgParse(config=None)
        mock_read_config.return_value = {'provider': {'name': 'provider_not_there'}}
        with self.assertRaisesRegex(VirgaException, 'Provider class not found'):
            virga()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_config')
    @patch('virga.asserts.get_provider_class')
    def test_virga_invokes_provider_validate_and_action(self, get_provider_class, *args):
        get_provider_class.return_value = MockProvider()
        virga()
        get_provider_class.return_value.validate.assert_called_once_with()
        get_provider_class.return_value.action.assert_called_once_with()
