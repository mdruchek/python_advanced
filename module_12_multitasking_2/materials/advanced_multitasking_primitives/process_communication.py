import time
import logging
import os
import multiprocessing
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySuperClass(object):

    def __init__(self, name):
        self.name = name
        pass

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        proc_pid = os.getpid()
        logger.info(f'{self.name} Doing something fancy in {proc_name}, pid {proc_pid} for {self.name}!')


class MyThread(threading.Thread):
    def __init__(self, i, queue):
        super().__init__()
        self.queue = queue
        self.obj = MySuperClass(f'Object num {i}')
        # self.i = i

    def run(self):
        time.sleep(1)
        self.obj.do_something()



def worker(queue: multiprocessing.Queue):
    while not queue.empty():
        obj = queue.get()
        obj.do_something()
        time.sleep(0.1)


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    pool = multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        initializer=worker,
        initargs=(queue,)
    )

    for i in range(1, 40):
        queue.put(MySuperClass(f'Object num {i}'))

    # prevent adding anything more to the queue and wait for queue to empty
    queue.close()
    queue.join_thread()

    # prevent adding anything more to the process pool and wait for all
    # processes to finish
    pool.close()
    pool.join()
    # threads = []
    # for i in [1, 2, 3, 4]:
    #     thread = MyThread(i, queue)
    #     thread.start()
    #     threads.append(thread)
    #     # time.sleep(1)
    #     # thread.obj.do_something()
    #
    # for thread in threads:
    #     thread.join()



