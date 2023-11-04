import logging.config
from logging_config import dict_config


logging.config.dictConfig(dict_config)


# root_logger = logging.getLogger()
#
sub_1 = logging.getLogger('sub_1')
# sub_1.setLevel('INFO')
# sub_1_logger.propagate = True
#
sub_2 = logging.getLogger('sub_2')
# sub_2_logger.propagate = False
#
# sub_sub_1 = logging.getLogger('sub_sub_1')
# sub_sub_1.setLevel('DEBUG')
#
# formatter = logging.Formatter(fmt='%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d')
#
# custom_handler = logging.StreamHandler()
# custom_handler.setLevel('DEBUG')
# custom_handler.setFormatter(formatter)
#
# file_handler = logging.FileHandler('applog.log', mode='a')
# file_handler.setFormatter(formatter)
#
# sub_1_logger.addHandler(custom_handler)
# sub_1_logger.addHandler(file_handler)
# sub_sub_1_logger.addHandler(custom_handler)


def main():
    sub_1.info('Сообщение от sub_1_logger')


if __name__ == '__main__':
    main()
