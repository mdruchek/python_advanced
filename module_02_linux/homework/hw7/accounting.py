"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = date[:4]
    month = int(date[4:6])
    day = int(date[6:])
    storage.setdefault(year, {}).setdefault(str(month), {}).setdefault(str(day), 0)
    storage[year].setdefault('total', 0)
    storage[year][str(month)].setdefault('total', 0)
    storage[year]['total'] += number
    storage[year][str(month)]['total'] += number
    storage[year][str(month)][str(day)] += number
    print(storage)
    return 'Данные сохранены.'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    if str(year) in storage:
        return f"За {year} год потрачено {storage[str(year)]['total']} рублей"
    else:
        return f'За {year} год траты не внесены.'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if str(year) in storage:
        if str(month) in storage[str(year)]:
            return f"За {month}.{year} потрачено {storage[str(year)][str(month)]['total']} рублей"
        else:
            return f'За {month}.{year} траты не внесены.'
    else:
        return f'За {year} год траты не внесены.'


if __name__ == "__main__":
    app.run(debug=True)
