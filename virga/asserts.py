import argparse
from importlib import import_module

import yaml
from yaml.parser import ParserError

from virga.exceptions import VirgaException


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    :rtype: Any
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('config', help='Test configuration file')
    arg_parser.add_argument('-definition', help='Definition file')
    arg_parser.add_argument('-logfile', help='Log file')
    arg_parser.add_argument('-debug', help='Show debug', action='store_true', default=False)
    arg_parser.add_argument('-silent', help='Do not output results', action='store_true', default=False)
    arg_parser.add_argument('-output', help='Resource output directory')
    return arg_parser.parse_args()


def read_config(config_path: str) -> dict:
    """
    Read, parse and return the configuration file.

    :param config_path: Configuration filename
    :return: Config structure
    """
    try:
        with open(config_path) as config_file:
            return yaml.load(config_file)
    except FileNotFoundError:
        raise VirgaException('Configuration file not found')
    except ParserError:
        raise VirgaException('Invalid configuration file')


def get_provider_class(config: dict, args: any) -> any:
    """
    Return an instance of the Provider based on the name in the configuration.

    :param config: Configuration structure
    :param args: Command line args
    :return: An instance of the Provider
    """
    try:
        provider = config['provider']['name']
    except (KeyError, TypeError):
        raise VirgaException('Provider missing')
    try:
        provider_module = import_module('virga.providers.%s' % provider)
        return provider_module.Provider(config, args)
    except ModuleNotFoundError:
        raise VirgaException('Provider module not found')
    except AttributeError:
        raise VirgaException('Provider class not found')


def virga():
    """
    The real deal.

    Calls the parser, reads the configuration, gets the Provider instantiated, calls the
    validator and starts the procedure.
    """
    args = parser()
    config = read_config(args.config)
    provider = get_provider_class(config, args)
    provider.validate()
    provider.action()
