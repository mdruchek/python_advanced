"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
from typing import List

from flask import Flask, request
import shlex
import subprocess


app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args: List[str] = request.args.getlist('arg')
    command_str = f'ps'
    command = shlex.split(command_str) + args
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True).stdout
    return f'<pre>{result}</pre>'


if __name__ == "__main__":
    app.run(debug=True)
