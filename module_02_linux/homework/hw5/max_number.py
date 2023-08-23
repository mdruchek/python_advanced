"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers):
    numbers = numbers.split('/')
    numbers = list(filter(filter_numbers, numbers))
    if len(numbers) > 0:
        max_number_var = max(map(float, numbers))
    else:
        return 'Числа не обнаружены!'
    return f'Максимальное переданное число {max_number_var}'


def filter_numbers(number: str):
    if number.find('-') == 0:
        number = number[1:]
    if number.find('.') == number.rfind('.'):
        number = f'{number[:number.find(".")]}{number[number.find(".") + 1:]}'
    if number.isdigit():
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(debug=True)
