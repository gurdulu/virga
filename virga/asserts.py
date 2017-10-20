import argparse
from importlib import import_module

import yaml
from yaml.parser import ParserError

from virga.exceptions import VirgaException


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('provider', help='Provider')
    arg_parser.add_argument('test_file', help='Test configuration file')
    arg_parser.add_argument('-p', '--param', nargs='*', help='Provider parameters (format key=value)')
    arg_parser.add_argument('-d', '--definition', help='Definition file')
    arg_parser.add_argument('-l', '--logfile', help='Log file')
    arg_parser.add_argument('-s', '--silent', help='Do not output results', action='store_true', default=False)
    arg_parser.add_argument('-o', '--output', help='Resource output directory')
    arg_parser.add_argument('--debug', help='Show debug', action='store_true', default=False)
    return arg_parser.parse_args()


def read_test_file(test_file_path: str) -> dict:
    """
    Read, parse and return the test configuration file.

    :param test_file_path: Test configuration filename
    :return: Test structure
    """
    try:
        with open(test_file_path) as test_file:
            return yaml.load(test_file)
    except FileNotFoundError:
        raise VirgaException('Test file not found')
    except ParserError:
        raise VirgaException('Invalid test file')


def get_provider_class(tests: dict, args: any) -> any:
    """
    Return an instance of the Provider based on the name in the configuration.

    :param tests: Tests to execute
    :param args: Command line args
    :return: An instance of the Provider
    """
    try:
        provider_module = import_module('virga.providers.%s' % args.provider)
        return provider_module.Provider(tests, args)
    except ModuleNotFoundError:
        raise VirgaException('Provider module not found')
    except AttributeError:
        raise VirgaException('Provider class not found')


def asserts():
    """
    The real deal.

    Calls the parser, reads the configuration, gets the Provider instantiated, calls the
    validator and starts the procedure.
    """
    args = parser()
    tests = read_test_file(args.test_file)
    provider = get_provider_class(tests, args)
    provider.validate()
    provider.action()
