import datetime
import random
import os
import re
from flask import Flask

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/hello_world')
def helo_word() -> str:
    return 'Hello Word!'


cars_list = 'Chevrolet, Renault, Ford, Lada'


@app.route('/cars')
def cars_func() -> str:
    return cars_list


cats_list = ['корниш-рекс',
             'русская голубая',
             'шотландская вислоухая',
             'мейн-кун',
             'манчкин']


@app.route('/cats')
def cats_func() -> str:
    return random.choice(cats_list)


@app.route('/get_time/now')
def time_now() -> str:
    current_time = datetime.datetime.now()
    text = f'Точное время: {current_time}'
    return text


@app.route('/get_time/future')
def time_future() -> str:
    current_time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    text = f'Точное время через час будет {current_time_after_hour}'
    return text


BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')


def filter_list(word):
    if word not in ['-', '[', ']', '***']:
        return True
    return False


def get_list(path_file):
    with open(path_file, 'r', encoding='utf-8') as file:
        list_from_file = list(filter(filter_list, [re.sub(r'[.,"\'-?:!;]', '', word) for line in file for word in line.split()]))
        return list_from_file


list_from_file = get_list(BOOK_FILE)


@app.route('/get_random_word')
def get_random_word():
    word = random.choice(list_from_file)
    return word


@app.route('/counter')
def counter():
    counter.visits += 1
    text = f'Вы поситили данную страницу {counter.visits} раз.'
    return text


counter.visits = 0


if __name__ == '__main__':
    app.run(debug=True)
