import datetime
import sqlite3


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    sql = """
        INSERT INTO `table_birds`
            (name, date)
        VALUES
            (?, ?);
    """

    cursor.execute(sql, (bird_name, date_time))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    sql = """
        SELECT *
            FROM `table_birds`
            WHERE name = ?;
    """

    cursor.execute(sql, (bird_name,))
    bird = cursor.fetchone()
    if bird:
        return True
    return False


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        log_bird(cursor, name, right_now)
