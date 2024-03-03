import json
import os
import time
from statistics import mean
from typing import List
import logging
from multiprocessing import Semaphore
from multiprocessing.pool import ThreadPool
import threading

import requests

from app.models import get_last_id_book


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def execution_time_meter(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start
        logger.info(f'Execution time: {execution_time}')
        return result
    return wrapper


class LibraryClient:
    URL_BOOKS: str = 'http://127.0.0.1:5000/api/books'
    URL_AUTHORS: str = 'http://127.0.0.1:5000/api/authors'
    TIMEOUT: int = 100

    def __init__(self, using_session: bool):
        self.using_session = using_session

        if using_session:
            self.parent_request = requests.Session()
        else:
            self.parent_request = requests
        self.session = requests.Session()

    def get_all_books(self, *args, **kwargs) -> List[dict]:
        response = self.parent_request.get(self.URL_BOOKS, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict, *args, **kwargs) -> dict:
        response = self.parent_request.post(self.URL_BOOKS, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_book(self, book_id: int) -> dict:
        response = self.parent_request.get(f'{self.URL_BOOKS}/{book_id}', timeout=self.TIMEOUT)
        return response.json()

    def complete_book_update(self, book_id, data: dict) -> dict:
        response = self.parent_request.put(f'{self.URL_BOOKS}/{book_id}', json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def partial_book_update(self, book_id, data: dict) -> dict:
        response = self.parent_request.patch(f'{self.URL_BOOKS}/{book_id}', json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def del_book(self, book_id: int) -> None:
        self.parent_request.delete(f'{self.URL_BOOKS}/{book_id}', timeout=self.TIMEOUT)

    def get_all_authors(self) -> List[dict]:
        response = self.parent_request.get(self.URL_AUTHORS, timeout=self.TIMEOUT)
        return response.json()

    def add_new_authors(self, data: dict):
        response = self.parent_request.post(self.URL_AUTHORS, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_author(self, author_id: int) -> dict:
        response = self.parent_request.get(f'{self.URL_AUTHORS}/{author_id}', timeout=self.TIMEOUT)
        return response.json()

    def del_author(self, author_id: int) -> None:
        self.parent_request.delete(f'{self.URL_AUTHORS}/{author_id}', timeout=self.TIMEOUT)


class SpeedTests:
    def __init__(self, number_requests: int, multithreading: bool, using_session: bool) -> None:
        self.number_requests = number_requests
        self.multithreading = multithreading
        self.using_session = using_session
        self.client = LibraryClient(using_session=using_session)

    def speed_test_post(self, method):
        data = (
            '{{'
                '"title": "title book {0}",'
                '"author": {{'
                    '"first_name": "author firstname {0}",'
                    '"last_name": "author lastname {0}",'
                    '"middle_name": "author middle name {0}"'
                '}}'
            '}}'
        )
        start_id = get_last_id_book() + 1
        if self.multithreading:
            with ThreadPool(processes=4) as thread_pool:
                thread_pool.map(
                    method,
                    (
                        json.loads(data.format(number_request + start_id))
                        for number_request
                        in range(self.number_requests)
                    )
                )
        else:
            start_id = get_last_id_book() + 1
            for number_request in range(self.number_requests):
                number_data = start_id + number_request
                method(json.loads(data.format(number_data)))

    def speed_test_get(self, method):
        if self.multithreading:
            with ThreadPool(processes=10) as thread_pool:
                threads = []
                for number_request in range(self.number_requests):
                    threads.append(thread_pool.apply_async(method))
                for thread in threads:
                    thread.wait()
        else:
            for number_request in range(self.number_requests):
                method()


if __name__ == '__main__':
    for number_requests in [10, 100, 1000]:
        test1 = SpeedTests(number_requests=number_requests, multithreading=False, using_session=False)
        test2 = SpeedTests(number_requests=number_requests, multithreading=False, using_session=True)
        test3 = SpeedTests(number_requests=number_requests, multithreading=True, using_session=False)
        test4 = SpeedTests(number_requests=number_requests, multithreading=True, using_session=True)
        tests = [test1, test2, test3, test4]
        for test in tests:
            execute_times = []
            for _ in range(5):
                start = time.time()
                # test.speed_test_get(test.client.get_all_books)
                test.speed_test_post(test.client.add_new_book)
                execute_time = time.time() - start
                execute_times.append(execute_time)
            logger.info('Number requests {num_req} '
                        'Used session: {session}. '
                        'Used multithreading: {multithreading}. '
                        'Average execute time: {mean:.4}.'
                        .format(num_req=number_requests,
                                session=test.using_session,
                                multithreading=test.multithreading,
                                mean=mean(execute_times)))
