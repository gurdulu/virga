import argparse

import sys

from virga.common import get_provider_class, VirgaException


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('provider', help='Provider')
    arg_parser.add_argument('section', help='Section')
    arg_parser.add_argument('resource', help='Resource ID')
    arg_parser.add_argument('-d', '--definition', help='Definition file')
    return arg_parser.parse_args()


def samples():
    """
    The other real deal.

    Calls the parser, gets the Provider instantiated, starts the procedure.
    """
    try:
        args = parser()
        provider = get_provider_class(args)
        return provider.sample(args.section, args.resource)
    except VirgaException as ex:
        sys.stderr.write(str(ex))
        sys.exit(1)
