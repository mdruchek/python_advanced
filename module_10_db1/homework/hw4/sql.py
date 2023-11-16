import sqlite3


with sqlite3.connect("hw_4_database.db") as conn:
    cursor = conn.cursor()

    cursor.execute(
        "SELECT count(*) "
        "FROM salaries "
        "WHERE salary < 5000;"
    )
    print(cursor.fetchone())

    cursor.execute(
        "SELECT round(avg(salary), 0) "
        "FROM salaries;"
    )
    print(cursor.fetchone())

    cursor.execute(
        "SELECT max(salary) "
        "FROM "
            "(SELECT salary "
            "FROM salaries "
            "ORDER BY salary "
            "LIMIT (SELECT count(salary) FROM salaries) / 2)"
    )
    print(cursor.fetchone())

    cursor.execute(
        "SELECT round(100 * (1.0 * top10) / (1.0 * bottom), 2) f "
        "FROM "
            "( "
                "SELECT sum(salary) bottom "
                "FROM "
                    "( "   
                        "SELECT salary "
                        "FROM "
                            "salaries "
                        "ORDER BY salary "
                        "LIMIT 0.9 * (SELECT count(salary) FROM salaries) "
                ") "
            "), "
            "( "
                "SELECT sum(salary) top10 "
                "FROM "
                    "( "
                        "SELECT salary "
                        "FROM "
                            "salaries "
                        "ORDER BY salary DESC " 
                        "LIMIT 0.1 * (SELECT count(salary) FROM salaries) "
                ") "
            ") "
    )
    print(cursor.fetchone())
