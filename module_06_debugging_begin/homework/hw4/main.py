"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
# from datetime import datetime
import datetime
import json
from typing import Dict
from itertools import groupby


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    task = {}
    for k, g in groupby(sorted(logs, key=lambda x: x['level']), lambda x: x["level"]):
        task.update({k: len(list(g))})
    return task


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    hour: int = 0
    count_max: int = 0
    for k, g in groupby(logs, lambda x: x["time"][:2]):
        count_temp = len(list(g))
        if count_temp > count_max:
            hour = int(k)
            count_max = count_temp
    return hour


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    logs_filter = filter(
        lambda x: datetime.time(5, 0, 0)
                  < datetime.time(int(x["time"][:2]), int(x["time"][3:5]), int(x["time"][6:9]))
                  < datetime.time(5, 20, 0)
                  and x["level"] == 'CRITICAL', logs)
    return len(list(logs_filter))


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    pass


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    pass


if __name__ == '__main__':
    with open("skillbox_json_messages.log", "r", encoding="utf-8") as file:
        logs = [json.loads(dic) for dic in file.read().split('\n') if dic]
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
