import sqlite3


with sqlite3.connect("hw_3_database.db") as conn:
    cursor = conn.cursor()

    #Вопрос 1
    cursor.execute(
        "SELECT count(*)"
        "FROM table_1;"
    )
    print(cursor.fetchone())

    cursor.execute(
        "SELECT count(*)"
        "FROM table_2;"
    )
    print(cursor.fetchone())

    cursor.execute(
        "SELECT count(*)"
        "FROM table_3;"
    )
    print(cursor.fetchone())

    #Вопрос 2
    cursor.execute(
        "SELECT DISTINCT count(*)"
        "FROM table_1;"
    )
    print(cursor.fetchone())

    # Вопрос 3
    cursor.execute(
        "SELECT count(*) "
        "FROM "
            "(SELECT table_1.id, value "
            "FROM table_1 "
            "INTERSECT "
            "SELECT id, value "
            "FROM table_2);"
    )
    print(cursor.fetchone())

    # Вопрос 4
    cursor.execute(
        "SELECT count(*) "
        "FROM "
        "table_1 "
        "INNER JOIN table_2 USING (id, value) "
        "INNER JOIN table_3 USING (id, value);"
    )
    print(cursor.fetchone())
