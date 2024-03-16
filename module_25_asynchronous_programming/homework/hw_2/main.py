import asyncio
import time
from pathlib import Path
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from typing import Callable

import aiohttp
import aiofiles
import requests


URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat_async(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        result = await response.read()
        await write_to_disk_async(result, idx)


async def write_to_disk_async(content: bytes, id: int):
    file_path = "{}/async/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats_async():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat_async(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def write_to_disk_blocking(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


def get_cat_blocking(idx: int):
    response = requests.get(URL)
    write_to_disk_blocking(response.content, idx)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Время выполнения функции {func.__name__}: ' + str(time.time() - start))
        return result
    return wrapper


@timer
def asyncio_cats():
    res = asyncio.run(get_all_cats_async())


@timer
def threads_cats():
    with ThreadPool(processes=8) as pool:
        pool.map(get_cat_blocking, range(CATS_WE_WANT))


@timer
def processes_cats():
    with Pool(processes=8) as pool:
        pool.map(get_cat_blocking, range(CATS_WE_WANT))


if __name__ == '__main__':
    asyncio_cats()
    threads_cats()
    processes_cats()
