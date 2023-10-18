"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import os
from subprocess import Popen, PIPE, TimeoutExpired
import shlex
from shlex import quote
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
    safe_code = shlex.quote(code)
    cmd = shlex.split(f"prlimit --nproc=1:1 python -c {safe_code}")
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE,  text=True)
    proc_kill = False
    try:
        outs, errs = proc.communicate(timeout=timeout)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        proc_kill = True

    return outs, errs, proc_kill


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        outs, errs, proc_kill = run_python_code_in_subprocess(code, timeout)
        if proc_kill:
            return f'Исполнение кода не уложилось в {timeout}сек.'
        return f'Вывод:<br>{outs}<br><br>Ошибки:<br>{errs}'
    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
