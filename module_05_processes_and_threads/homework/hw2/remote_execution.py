"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import os
from subprocess import Popen, PIPE, TimeoutExpired
from time import time
from typing import Tuple

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=30)])


def run_python_code_in_subprocess(code: str, timeout: int) -> Tuple:
    start = time()
    cmd = f'prlimit --nproc=1:1 python -c "{code}"'
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE,  text=True)
    try:
        outs, errs = proc.communicate(timeout=timeout, input=f'Исполнение кода не уложилось в {timeout}сек.')
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        outs = f'<h1>Исполнение кода не уложилось в {timeout}сек.</h1>' + outs

    return outs, errs


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        outs, errs = run_python_code_in_subprocess(code, timeout)
        return f'Вывод:<br>{outs}<br><br>Ошибки:<br>{errs}'
    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
