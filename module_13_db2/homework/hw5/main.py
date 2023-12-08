import sqlite3
import random
import string


countries = (
    'Россия',
    'Англия',
    'Франция',
    'Германия',
    'Чехия',
    'Украина',
    'Словакия',
    'Италия',
    'Греция',
    'Белорусия',
    'Нидерланды'
)

command_levels = [
    'сильная',
    'средняя',
    'средняя',
    'слабая'
]

commands_name = []


insert_uefa_command_table_sql = """
    INSERT INTO `uefa_commands`
    (command_name, command_country, command_level)
    VALUES
    (?, ?, ?);
"""

insert_uefa_draw_table_sql = """
    INSERT INTO `uefa_draw`
    (command_number, group_number)
    VALUES
    (?, ?);
"""


select_commands_by_level = """
    SELECT `command_number`
        FROM `uefa_commands`
        WHERE `command_level` = ?;
"""


delete_data_in_tables_sql = """
    DELETE FROM `uefa_commands`;
    DELETE FROM `uefa_draw`;
"""


def get_commands_name(number_command: int):
    while len(commands_name) < number_command:
        name_command = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)]).capitalize()
        if name_command not in commands_name:
            commands_name.append(name_command)
    return commands_name


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    cursor.executescript(delete_data_in_tables_sql)
    get_commands_name(number_of_groups * 4)
    full_commands_level = command_levels * number_of_groups
    random.shuffle(full_commands_level)

    commands = [
        (
            commands_name.pop(),
            random.choice(countries),
            full_commands_level.pop()
        ) for _ in range(number_of_groups * 4)
    ]

    cursor.executemany(insert_uefa_command_table_sql, commands)

    for level in set(command_levels):
        cursor.execute(select_commands_by_level, (level,))
        commands_id = cursor.fetchall()
        groups = [x for x in range(1, number_of_groups + 1)]

        if level == 'средняя':
            groups *= 2

        random.shuffle(groups)

        for command_id, group in zip(commands_id, groups):
            cursor.execute(insert_uefa_draw_table_sql, (command_id[0], group))


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
