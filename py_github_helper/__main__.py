import logging
from .utils.custom_arg_parser import parse_args, get_logging_level


if __name__ == "__main__":
    log_level = get_logging_level()
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
    logging.info(parse_args())
    exit(0)
