import sqlite3


sql_script_to_execute = """
    UPDATE `table_russian_post`
        SET `order_day` = '01-05-2023'
        WHERE `order_id` IN
                            (SELECT 
                                    `order_id`
                                FROM 
                                    `table_russian_post`
                                WHERE
                                    `order_day` LIKE '%-05-2023')
"""

if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script_to_execute)
        conn.commit()
