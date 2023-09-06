import datetime

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = date[:4]
    month = int(date[4:6])
    day = int(date[6:])
    datetime.datetime(int(year), month, day)
    storage.setdefault(year, {}).setdefault(str(month), {}).setdefault(str(day), 0)
    storage[year].setdefault('total', 0)
    storage[year][str(month)].setdefault('total', 0)
    storage[year]['total'] += number
    storage[year][str(month)]['total'] += number
    storage[year][str(month)][str(day)] += number
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


@app.route("/remove_storage/")
def remove_storage():
    if app.config['TESTING']:
        global storage
        storage = {}
        return 'storage обнулился'
    else:
        return 'Метод для тестового режима!'


@app.route("/get_storage/")
def get_storage():
    if app.config['TESTING']:
        global storage
        return storage
    else:
        return 'Метод для тестового режима!'


if __name__ == "__main__":
    app.run(debug=True)
