import time
import random
import logging
from typing import List
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

import requests
import threading
import sqlite3


semaphore = threading.Semaphore(4)
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def create_tables_database() -> None:
    con = sqlite3.connect('swapi.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE if not exists people(name NCHAR, birth_year NCHAR, gender NCHAR)')


def get_characters_num() -> List:
    return random.sample(range(1, 84), k=20)


def save_character(char_num: int) -> None:
    response: requests.Response = requests.get(f'https://swapi.dev/api/people/{char_num}/')
    if response.status_code != 200:
        return
    print(response.json())
    saving_to_database(response.json())


def saving_to_database(data: dict):
    con = sqlite3.connect('swapi.db')
    cur = con.cursor()
    cur.execute("""
        INSERT INTO people (name, birth_year, gender)
        VALUES ('{name}', '{birth_year}', '{gender}')
    """.format(name=data['name'],
               birth_year=data['birth_year'],
               gender=data['gender']))
    con.commit()
    con.close()


# def load_characters_sequential(chars_num: List) -> None:
#     start: float = time.time()
#     for char_num in chars_num:
#         save_character(char_num)
#     logger.info('The sequential download ended in {:.4}'.format(time.time() - start))
#
#
# def load_characters_multithreading(chars_num: List) -> None:
#     start: float = time.time()
#     threads: List[threading.Thread] = []
#     for char_num in chars_num:
#         with semaphore:
#             thread = threading.Thread(target=save_character, args=[char_num])
#             thread.start()
#             threads.append(thread)
#
#     for thread in threads:
#         thread.join()
#     logger.info('The sequential download ended in {:.4}'.format(time.time() - start))


def load_characters_pool(chars_num: List) -> None:
    start: float = time.time()
    with Pool(processes=cpu_count()) as pool:
        pool.map(save_character, chars_num)
    logger.info('The pool download ended in {:.4}'.format(time.time() - start))


def load_characters_threadpool(chars_num: List) -> None:
    start: float = time.time()
    with ThreadPool(processes=cpu_count() * 5) as threadpool:
        threadpool.map(save_character, chars_num)
    logger.info('The threadpool download ended in {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    create_tables_database()
    characters_num = get_characters_num()
    # load_characters_sequential(characters_num)
    # load_characters_multithreading(characters_num)
    load_characters_pool(characters_num)
    load_characters_threadpool(characters_num)
