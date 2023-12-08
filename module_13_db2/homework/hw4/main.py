import sqlite3

NAME_EFFECTIVE_MANAGER = 'Иван Совин'

sql_get_salary = """
    SELECT `salary`
        FROM `table_effective_manager`
        WHERE name = ?;
"""

sql_increase_salary = """
    UPDATE `table_effective_manager`
        SET `salary` = ?
        WHERE `name` = ?;
"""


sql_drop_employee = """
    DELETE FROM `table_effective_manager`
        WHERE name = ?;
"""


def get_salary(cursor: sqlite3.Cursor, name: str):
    cursor.execute(sql_get_salary, (name,))
    salary, *_ = cursor.fetchone()
    return salary


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    salary_employee = get_salary(cursor, name)
    salary_after_promotion = salary_employee + salary_employee * 0.1
    if salary_after_promotion <= SALARY_EFFECTIVE_MANAGER:
        cursor.execute(sql_increase_salary, (salary_after_promotion, name))
    else:
        cursor.execute(sql_drop_employee, (name,))


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        SALARY_EFFECTIVE_MANAGER = get_salary(cursor, NAME_EFFECTIVE_MANAGER)
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
