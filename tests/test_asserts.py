from unittest import TestCase

import sys
from unittest.mock import patch, mock_open

import os

from tests import MockProvider, fixture, fixtures_dir

# https://stackoverflow.com/questions/8658043/how-to-mock-an-import
sys.modules['virga.providers.provider_not_there'] = __import__('unittest.mock')

from virga.asserts import asserts, parser, read_testfile  # NOQA
from virga.common import VirgaException  # NOQA


class TestVirgaAsserts(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('-p', '--provider', choices=['aws', ], required=True, help='provider')
        mock_add_argument.assert_any_call('-t', '--testfile', nargs='+', required=True, help='test file')
        mock_add_argument.assert_any_call('-d', '--definitions', help='custom definitions path')
        mock_add_argument.assert_any_call('-l', '--logfile', help='redirect the output to a log file')
        mock_add_argument.assert_any_call('-s', '--silent', help='do not output results', action='store_true', default=False)
        mock_add_argument.assert_any_call('-o', '--output', help='save the resource info into the specified directory')
        mock_add_argument.assert_any_call('--debug', help='show debug', action='store_true', default=False)
        mock_parse_args.assert_called_once()

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_testfile')
    @patch('virga.asserts.get_provider_class')
    def test_virga_function_invoke_parser_and_read_testfile(self, mock_get_provider_class, mock_read_testfile, mock_parser):
        asserts()
        mock_parser.assert_called_once_with()
        mock_read_testfile.assert_called_once()
        mock_get_provider_class.assert_called_once()

    def test_read_multiple_testfiles(self):
        paths = [
            os.path.join(fixtures_dir, 'multi-test1.yaml'),
            os.path.join(fixtures_dir, 'multi-test2.yaml'),
        ]
        expected = {
            'my-multi-test1': {
                'test': 'test'
            },
            'my-multi-test2': {
                'test': 'test'
            },
        }
        self.assertDictEqual(expected, read_testfile(paths))

    def test_not_existing_testfile_raise_virga_exc(self):
        with self.assertRaisesRegex(VirgaException, 'Test file not found'):
            read_testfile(['test-file-not-here.yaml', ])

    def test_invalid_testfile_raise_virga_exc(self):
        with patch('builtins.open', mock_open(read_data=fixture('invalid.yaml'))) as _:
            with self.assertRaisesRegex(VirgaException, 'Invalid test file'):
                read_testfile(['test-file-not-here.yaml', ])

    @patch('virga.asserts.parser')
    @patch('virga.asserts.read_testfile')
    @patch('virga.asserts.get_provider_class')
    def test_virga_invokes_provider_validate_and_action(self, get_provider_class, *args):
        get_provider_class.return_value = MockProvider()
        asserts()
        get_provider_class.return_value.action.assert_called_once_with()
