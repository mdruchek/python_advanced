import sqlite3
import csv


sql_removes_penalty = """
    DELETE
        FROM `table_fees`
        WHERE `truck_number` = ?;
"""


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file) as file:
        for row in csv.reader(file):
            print(row)
            if row[0] != 'car_number':
                cursor.execute(sql_removes_penalty, (row[0],))


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
