import sqlite3


sql_request = """
    SELECT
        COUNT(*)
    FROM
        `table_kotlin`
    WHERE
        `wind` > 32;
"""


def get_number_hurricane_days(cursor: sqlite3.Cursor) -> int:
    cursor.execute(sql_request)
    num_hurricane, *_ = cursor.fetchone()
    return num_hurricane


if __name__ == '__main__':
    con = sqlite3.connect('practise.db')
    cursor = con.cursor()
    num_hurricane_days = get_number_hurricane_days(cursor)
    print(f'Количество ураганных дней составляет {num_hurricane_days}')
