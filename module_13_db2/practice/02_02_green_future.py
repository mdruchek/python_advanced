import sqlite3
from calendar import monthrange


sql_request = """
    SELECT
        COUNT(*)
    FROM
        `table_green_future`
    WHERE
        strftime('%m', `date`) = ? AND
        action LIKE 'отнесли мешки на завод'        
"""


def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:
    if len(str(month_number)) == 1:
        month_number = str(f'0{month_number}')
    c.execute(sql_request, (str(month_number),))
    num_days, *_ = c.fetchone()
    days = monthrange(2022, month_number)[1]
    return num_days/days


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
