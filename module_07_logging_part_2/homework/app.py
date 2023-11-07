import logging.config
import sys

import logging_tree

from utils import string_to_operator
from logging_config import dict_config, dict_config_from_ini


app_logger = logging.getLogger('app')
logging.config.dictConfig(dict_config)

# applogger = logging.getLogger('appLogger')
# logging.config.dictConfig(dict_config_from_ini)


with open('logging_tree.txt', 'w') as file:
    file.write(logging_tree.format.build_description())


def calc(args):
    app_logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        app_logger.error("Error while converting number 1")
        app_logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        app_logger.error("Error while converting number 1")
        app_logger.exception(e)

    operator_func = string_to_operator(operator)
    result = operator_func(num_1, num_2)

    app_logger.debug(f"Result: {result}")
    app_logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    calc(sys.argv[1:])
