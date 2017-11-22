from unittest import TestCase
from unittest.mock import patch

from tests import MockProvider
from virga.common import VirgaException
from virga.samples import parser, samples


class TestVirgaSamples(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('provider', help='Provider')
        mock_add_argument.assert_any_call('section', help='Section')
        mock_add_argument.assert_any_call('resource', help='Resource ID')
        mock_add_argument.assert_any_call('-d', '--definitions', help='Definitions path')
        mock_parse_args.assert_called_once()

    @patch('virga.samples.parser')
    @patch('virga.samples.get_provider_class')
    def test_samples_invoke_class_samples(self, mock_get_provider_class, *args):
        mock_get_provider_class.return_value = MockProvider()
        samples()
        mock_get_provider_class.return_value.sample.assert_called_once()

    @patch('virga.samples.parser')
    def test_any_virga_exception_is_caught(self, mock_parser):
        mock_parser.side_effect = VirgaException('Any exception')
        with self.assertRaises(SystemExit) as ex:
            samples()
        self.assertEqual(1, ex.exception.code)
