import sys
import time
from math import factorial
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

sys.set_int_max_str_digits(0)


def high_load():
    start = time.time()
    input_values = list([i for i in range(10000)])

    with Pool(processes=4) as pool:
        result = sum(pool.map(factorial, input_values))

    end = time.time()
    print(result)
    print(end-start)


if __name__ == '__main__':
    high_load()
