"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: list) -> float:
    total_file_size: int = 0
    numbers_file: int = len(ls_output)
    if numbers_file:
        for line in ls_output:
            total_file_size += int(line.split()[4])
        average_file_size: float = total_file_size / numbers_file
        return average_file_size
    return 0


if __name__ == '__main__':
    data: list = sys.stdin.readlines()[1:]
    mean_size: float = get_mean_size(data)
    print(mean_size)
