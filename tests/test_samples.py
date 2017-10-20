from unittest import TestCase
from unittest.mock import patch

from virga.samples import parser


class TestVirgaSamples(TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.add_argument')
    def test_parser_function(self, mock_add_argument, mock_parse_args):
        parser()
        mock_add_argument.assert_any_call('provider', help='Provider')
        mock_add_argument.assert_any_call('section', help='Section')
        mock_add_argument.assert_any_call('resource', help='Resource ID')
        mock_parse_args.assert_called_once()
