import logging
from .utils.custom_arg_parser import parse_args


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.ERROR)
    print(parse_args())
    exit(0)
