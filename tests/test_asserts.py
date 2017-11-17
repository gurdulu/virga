from unittest import TestCase

import sys
from unittest.mock import patch, mock_open

from tests import MockProvider, fixture

# https://stackoverflow.com/questions/8658043/how-to-mock-an-import
sys.modules['virga.providers.provider_not_there'] = __import__('unittest.mock')

from virga.asserts import asserts, parser, read_test_file  # NOQA
from virga.common import VirgaException  # NOQA


class TestVirgaAsserts(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('provider', help='Provider')
        mock_add_argument.assert_any_call('test_file', help='Test configuration file')
        mock_add_argument.assert_any_call('-d', '--definition', help='Definition file')
        mock_add_argument.assert_any_call('-l', '--logfile', help='Log file')
        mock_add_argument.assert_any_call('-s', '--silent', help='Do not output results', action='store_true', default=False)
        mock_add_argument.assert_any_call('-o', '--output', help='Resource output directory')
        mock_add_argument.assert_any_call('--debug', help='Show debug', action='store_true', default=False)
        mock_parse_args.assert_called_once()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_test_file')
    @patch('virga.asserts.get_provider_class')
    def test_virga_function_invoke_parser_and_read_test_file(self, mock_get_provider_class, mock_read_test_file, mock_parser):
        asserts()
        mock_parser.assert_called_once_with()
        mock_read_test_file.assert_called_once()
        mock_get_provider_class.assert_called_once()

    def test_not_existing_test_file_raise_virga_exc(self):
        with self.assertRaisesRegex(VirgaException, 'Test file not found'):
            read_test_file('test-file-not-here.yaml')

    def test_invalid_test_file_raise_virga_exc(self):
        with patch('builtins.open', mock_open(read_data=fixture('invalid.yaml'))) as _:
            with self.assertRaisesRegex(VirgaException, 'Invalid test file'):
                read_test_file('test-file-not-here.yaml')

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_test_file')
    @patch('virga.asserts.get_provider_class')
    def test_virga_invokes_provider_validate_and_action(self, get_provider_class, *args):
        get_provider_class.return_value = MockProvider()
        asserts()
        get_provider_class.return_value.action.assert_called_once_with()
