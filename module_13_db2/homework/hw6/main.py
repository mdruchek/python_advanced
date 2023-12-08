import datetime
import random
import sqlite3
from itertools import cycle


club_schedule = [
    'футбол',
    'хоккей',
    'шахматы',
    'SUP-сёрфинг',
    'бокс',
    'Dota2',
    'шахбокс'
]


delete_data_table_sql = """
    DELETE FROM `table_friendship_schedule`;
"""


get_users_sql = """
    SELECT `id`
        FROM `table_friendship_employees`
        WHERE `preferable_sport` != ?
        ORDER BY `id`
"""


insert_schedule_sql = """
    INSERT INTO `table_friendship_schedule`
    (`employee_id`, `date`)
    VALUES
    (?, '{}');
"""


def get_dates_days_week():
    week_days_list = []
    for weekday in range(7):
        d = datetime.datetime(datetime.date.today().year, 1, weekday + 1)
        week_days_list.append([])
        while d < datetime.datetime(datetime.date.today().year + 1, 1, 1):
            week_days_list[weekday].append(d)
            d += datetime.timedelta(days=7)
    return week_days_list


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    cursor.execute(delete_data_table_sql)
    for sport, weekdays in zip(club_schedule, get_dates_days_week()):
        cursor.execute(get_users_sql, (sport,))
        employees = cursor.fetchall()
        for day in weekdays:
            day = day.strftime("%d.%m.%Y")
            cursor.executemany(insert_schedule_sql.format(day),
                               random.choices(employees, k=10))


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
