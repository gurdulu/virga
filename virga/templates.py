import argparse


def parser() -> any:
    """
    Argument definition and parsing.

    :return: Arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('section', help='Section to analyse')
    arg_parser.add_argument('resource', help='Resource ID')
    return arg_parser.parse_args()