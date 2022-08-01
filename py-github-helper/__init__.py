import logging
import sys
from .custom_arg_parser import parse_args

def main(argv):
    parse_args(argv)

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    print(main(sys.argv[1:]))