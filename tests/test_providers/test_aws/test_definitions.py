import json
import os
from functools import wraps
from unittest import TestCase
from unittest.mock import patch

import yaml

from virga.providers import aws


def fixtures(**kwargs):
    def decorator(function):
        @wraps(function)
        def wrap(*args):
            with open(os.path.join(os.path.dirname(aws.__file__), 'definitions', kwargs['definition'])) as fp:
                definition_content = yaml.safe_load(fp)
            with open(os.path.join(os.path.dirname(__file__), 'fixtures', kwargs['response'])) as fp:
                fixture_content = json.load(fp)
            function(args[0], definition_content, fixture_content, *args[1:])
        return wrap
    return decorator


@patch('botocore.client.BaseClient._make_api_call')
class TestDefinitions(TestCase):

    def setUp(self):
        self.definition = None

    @fixtures(definition='addresses.yaml', response='addresses.json')
    def test_addresses(self, definition, response, *args):
        self.assertIn(definition['addresses']['prefix'], response)
        self.assertIn(definition['addresses']['resource_id'], response['Addresses'][0])
