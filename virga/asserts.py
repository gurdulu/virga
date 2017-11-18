import argparse
import yaml
from yaml.parser import ParserError

from virga.common import VirgaException, get_provider_class


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('provider', choices=['aws', ], help='provider')
    arg_parser.add_argument('testfile', help='test file')
    arg_parser.add_argument('-d', '--definition', help='custom definition file')
    arg_parser.add_argument('-l', '--logfile', help='redirect the output to a log file')
    arg_parser.add_argument('-s', '--silent', help='do not output results', action='store_true', default=False)
    arg_parser.add_argument('-o', '--output', help='save the resource info into the specified directory')
    arg_parser.add_argument('--debug', help='show debug', action='store_true', default=False)
    return arg_parser.parse_args()


def read_testfile(testfile_path: str) -> dict:
    """
    Read, parse and return the test configuration file.

    :param testfile_path: Test configuration filename
    :return: Test structure
    """
    try:
        with open(testfile_path) as testfile:
            return yaml.load(testfile)
    except FileNotFoundError:
        raise VirgaException('Test file not found')
    except ParserError:
        raise VirgaException('Invalid test file')


def asserts():
    """
    The real deal.

    Calls the parser, reads the test file, gets the Provider instantiated, starts the procedure.
    """
    args = parser()
    tests = read_testfile(args.testfile)
    provider = get_provider_class(args)
    provider.set_tests(tests)
    provider.action()
