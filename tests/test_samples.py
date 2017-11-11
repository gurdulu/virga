from unittest import TestCase
from unittest.mock import patch

from tests import MockProvider
from virga.samples import parser, samples


class TestVirgaSamples(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('provider', help='Provider')
        mock_add_argument.assert_any_call('section', help='Section')
        mock_add_argument.assert_any_call('resource', help='Resource ID')
        mock_add_argument.assert_any_call('-d', '--definition', help='Definition file')
        mock_parse_args.assert_called_once()

    @patch('virga.samples.parser')
    @patch('virga.samples.get_provider_class')
    def test_samples_invoke_class_samples(self, get_provider_class, *args):
        get_provider_class.return_value = MockProvider()
        samples()
        get_provider_class.return_value.sample.assert_called_once()
