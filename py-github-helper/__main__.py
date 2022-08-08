import logging
import sys
from .utils.custom_arg_parser import parse_args


def main(argv):
    return parse_args(argv)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.ERROR)
    print(main(sys.argv[1:]))
    exit(0)
