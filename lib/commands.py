


from lib.api import Api
from argparse import ArgumentParser


def arguement_parser():
    parser = ArgumentParser()
    # add global args
    subparsers = parser.add_subparsers(help='help text.')

    # connect parser
    connect_parser  = subparsers.add_parser('connect', help='connect help.')
    connect_parser.add_argument('name', help='Connection name.')
    connect_parser.set_defaults(func=Api.connect)

    # play parser
    play_parser     = subparsers.add_parser('play', help='play help.')
    play_parser.add_argument('filepath', help='File to play.')
    play_parser.set_defaults(func=Api.play)

    # generate parser
    generate_parser = subparsers.add_parser('generate', help='generate help.')
    generate_parser.add_argument('filepath', help='Configuration file.')
    generate_parser.set_defaults(func=Api.generate)

    return parser