import argparse
import sys
from importlib import import_module

import yaml
from yaml.parser import ParserError


class VirgaException(Exception):
    """Custom exception for Virga."""


def get_provider_class(args: any) -> any:
    """
    Return an instance of the Provider based on the name in the configuration.

    :param args: Command line args
    :return: An instance of the Provider
    """
    try:
        provider_module = import_module('virga.providers.%s' % args.provider)
        return provider_module.Provider(args)
    except ModuleNotFoundError:
        raise VirgaException('Provider module not found')
    except AttributeError:
        raise VirgaException('Provider class not found')


def read_testfile(testfile_paths: list) -> dict:
    """
    Read, parse and return the test configuration file.

    :param testfile_paths: Test configuration filename
    :return: Test structure
    """
    try:
        tests = {}
        for testfile_path in testfile_paths:
            with open(testfile_path) as testfile:
                tests.update(yaml.full_load(testfile))
        return tests
    except FileNotFoundError:
        raise VirgaException('Test file not found')
    except ParserError:
        raise VirgaException('Invalid test file')


def assert_parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--provider', choices=['aws', ], required=True, help='provider')
    arg_parser.add_argument('-t', '--testfile', nargs='+', required=True, help='test file')
    arg_parser.add_argument('-d', '--definitions', help='custom definitions path')
    arg_parser.add_argument('-l', '--logfile', help='redirect the output to a log file')
    arg_parser.add_argument('-s', '--silent', help='do not output results', action='store_true', default=False)
    arg_parser.add_argument('-o', '--output', help='save the resource info into the specified directory')
    arg_parser.add_argument('--processes', type=int, help='number of parallel processes Virga will instantiate')
    arg_parser.add_argument('--debug', help='show debug', action='store_true', default=False)
    return arg_parser.parse_args()


def assert_main():
    """
    The real deal.

    Calls the parser, reads the test file, gets the Provider instantiated, starts the procedure.
    """
    args = assert_parser()
    tests = read_testfile(args.testfile)
    provider = get_provider_class(args)
    provider.set_tests(tests)
    provider.action()


def sample_parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--provider', required=True, help='provider')
    arg_parser.add_argument('-s', '--section', required=True, help='type of resource to exemplify')
    arg_parser.add_argument('-r', '--resource', required=True, help='resource id')
    arg_parser.add_argument('-d', '--definitions', help='definitions path')
    return arg_parser.parse_args()


def sample_main():
    """
    The other real deal.

    Calls the parser, gets the Provider instantiated, starts the procedure.
    """
    try:
        args = sample_parser()
        provider = get_provider_class(args)
        return provider.sample(args.section, args.resource)
    except VirgaException as ex:
        sys.stderr.write(str(ex))
        sys.exit(1)
