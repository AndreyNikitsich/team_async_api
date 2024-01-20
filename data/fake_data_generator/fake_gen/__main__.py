from argparse import Namespace

from .arguments import parser
from .worker import do_work

args = parser.parse_args()

match args:
    case Namespace(dsn=''):
        parser.error('--dsn required\n')
    case Namespace():
        try:
            do_work(args.dsn, args.films, args.people, args.genres)
        except Exception as e:
            parser.error(e)
        parser.exit(0, 'Done')

    case _:
        parser.error('Incredible situation. Exit.')
