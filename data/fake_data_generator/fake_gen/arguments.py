import argparse

from .version import version


parser = argparse.ArgumentParser(
    prog='fake_gen',
    description=f'Fake data generator version {version}',
    epilog='Have a nice day!',
)

parser.add_argument(
    '--dsn',
    help='Postgresql connection string',
    type=str,
    default='',
)

parser.add_argument(
    '-v',
    '--version',
    help='Show self version and exit',
    action='version',
    default=argparse.SUPPRESS,
    version=version,
)

parser.add_argument(
    'films',
    metavar='films',
    help='Number of films',
    type=int,
    action='store',
)

parser.add_argument(
    'people',
    metavar='people',
    help='Number of people',
    type=int,
    action='store',
)

parser.add_argument(
    'genres',
    metavar='genres',
    help='Number of genres',
    type=int,
    action='store',
)
