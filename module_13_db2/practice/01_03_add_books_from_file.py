import sqlite3
import csv


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    with open(file_name) as file:
        reader = csv.reader(file)
        for num, row in enumerate(reader):
            print(num, row)
            if num != 0:
                cursor.execute("""
                    INSERT INTO 'table_books' (ISBN, book_name, author, publish_year) VALUES
                    (?,?,?,?);
                """, row)


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
