import logging
import sys
from .custom_arg_parser import parse_args

def main(argv):
    parse_args(argv)

def run():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    print(main(sys.argv[1:]))
