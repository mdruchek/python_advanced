"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import re
import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")


def read_word(file: str) -> list:
    logger.info("Чтание файла words")
    with open(file, 'r', encoding='latin-1') as fw:
        logger.info("Запись слов в массив")
        words = fw.read().split()
    return words


def extracting_words_from_password(password: str) -> list:
    logger.info("Извлечение всех слов из пароля")
    words_from_password_sum = []
    for n in range(4, len(password) + 1):
        words_from_password = re.findall(r"(?=([a-z, A-Z]{" + str(n) + "}))", password)
        words_from_password_sum += words_from_password
    return words_from_password_sum


def is_strong_password(password: str) -> bool:
    word_from_password = extracting_words_from_password(password)
    for word in word_from_password:
        if word.lower() in words:
            logger.info("Найдено слово в списке слов")
            return False
    return True


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()
    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif not is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.info("Пароль верный")
            return True
        logger.info("Пароль не верный")
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="stderr.txt",
        encoding="utf-8",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    words = read_word('words')
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
