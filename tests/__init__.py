import json
import os

import yaml
from unittest.mock import MagicMock

fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')


def fixture(filename, get_yaml=False, get_json=False):
    with open(os.path.join(fixtures, filename)) as f:
        if get_yaml:
            return yaml.load(f)
        elif get_json:
            return json.load(f)
        else:
            return f.read()


class MockArgParse(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.add_attribute(k, v)
        self.kwargs = kwargs

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)


class MockProvider(object):

    def __init__(self):
        self.action = MagicMock()
        self.lookup = MagicMock()
