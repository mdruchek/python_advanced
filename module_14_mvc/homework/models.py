import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, number_views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.number_views: int = number_views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    number_views INT
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author, number_views) VALUES (?, ?, 0)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        books_info = cursor.fetchall()
        if books_info:
            update_number_views_book(cursor, books_info)
            return [Book(*row) for row in books_info]


def get_books_by_author(author_name: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books` WHERE `author` = ?
            """,
            (author_name,)
        )
        books_info = cursor.fetchall()
        if books_info:
            update_number_views_book(cursor, books_info)
            return [Book(*row) for row in books_info]


def added_book(title, author) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `table_books`
            (title, author, number_views)
            VALUES
            (?, ?, 0)
            """,
            (title, author)
        )


def get_book_info(book_id) -> Book:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books` WHERE `id` = ?
            """,
            (book_id,)
        )
        book_info = cursor.fetchone()
        if book_info:
            update_number_views_book(cursor, [book_info])
            return Book(*book_info)


def update_number_views_book(cursor: sqlite3.Cursor, books_info: List[tuple]):
    for book_info in books_info:
        cursor.execute(
            """
            UPDATE `table_books`
            SET `number_views` = ?
            WHERE id = ?
            """,
            (book_info[3] + 1, book_info[0])
        )
