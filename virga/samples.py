import argparse

from virga.common import get_provider_class


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('provider', help='Provider')
    arg_parser.add_argument('section', help='Section')
    arg_parser.add_argument('resource', help='Resource ID')
    return arg_parser.parse_args()


def samples():
    """
    The other real deal.

    Calls the parser, gets the Provider instantiated, starts the procedure.
    """
    args = parser()
    provider = get_provider_class(args)
    provider.sample()
