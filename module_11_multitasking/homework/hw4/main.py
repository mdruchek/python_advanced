import random
import queue
import threading
import time
from threading import Lock, Semaphore
from queue import PriorityQueue


pq: queue.PriorityQueue = PriorityQueue(maxsize=10)
priorities = [x for x in range(10)]
LOCK = Lock()
SEMAPHORE = Semaphore()


def task(priority):
    print(f'running Task(priority={priority})')


class Producer(threading.Thread):
    def __init__(self, priority_queue, semaphore):
        super().__init__()
        self.sem = semaphore
        self.pq: queue.PriorityQueue = priority_queue
        print('Producer: Running')

    def __del__(self):
        print('Producer: Done')

    def run(self) -> None:
        while not self.pq.full():
            with SEMAPHORE:
                self.pq.put((priorities.pop(random.randint(0, len(priorities) - 1)), task))


class Consumer(threading.Thread):
    def __init__(self, priority_queue, semaphore):
        super().__init__()
        self.sem = semaphore
        self.pq: queue.PriorityQueue = priority_queue
        print('Consumer: Running')

    def __del__(self):
        print('Consumer: Done')

    def run(self) -> None:
        while not self.pq.empty():
            with SEMAPHORE:
                priority, task = self.pq.get()
                task(priority)
                pq.task_done()


if __name__ == '__main__':
    producer = Producer(pq, SEMAPHORE)
    consumer = Consumer(pq, SEMAPHORE)

    producer.start()
    consumer.start()
