import random
import time

import queue
import threading

import requests


def writer_logs(file, timestamp, date):
    with open(file, 'a') as file:
        file.write(f'{timestamp}, {date}\n')
        time.sleep(random.random())


class Worker(threading.Thread):
    def __init__(self, q) -> None:
        super().__init__()
        self.queue: queue.Queue = q

    def run(self) -> None:
        start = time.time()
        while time.time() - start <= 20:
            timestamp = time.time()
            response = requests.get(f'http://127.0.0.1:8080/timestamp/{timestamp}')
            self.queue.put((timestamp, response.text))
            writer_logs('log_not_sorted.log', timestamp, response.text)
            time.sleep(1)


class Logger(threading.Thread):
    def __init__(self, q) -> None:
        super().__init__()
        self.queue: queue.Queue = q

    def run(self) -> None:
        while not self.queue.empty():
            timestamp, date = self.queue.get()
            writer_logs('log_sorted.log', timestamp, date)


if __name__ == '__main__':
    queue = queue.Queue()

    start = time.time()
    threads = []
    for _ in range(10):
        thread = Worker(queue)
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for thread in threads:
        thread.join()

    log_thread = Logger(queue)
    log_thread.start()
