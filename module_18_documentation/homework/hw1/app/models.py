import os
import pathlib
import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = {
    'books': [
        {'book_id': 1, 'book_title': 'Война и мир', 'auth_id': 1},
        {'book_id': 2, 'book_title': 'Незнайка и его друзья', 'auth_id': 2},
        {'book_id': 3, 'book_title': 'Капитанская дочка', 'auth_id': 3},
    ],
    'authors': [
        {'auth_id': 1, 'auth_first_name': 'Лев', 'auth_last_name': 'Толстой', 'auth_middle_name': 'Николаевич'},
        {'auth_id': 2, 'auth_first_name': 'Николай', 'auth_last_name': 'Носов', 'auth_middle_name': 'Николаевич'},
        {'auth_id': 3, 'auth_first_name': 'Александр', 'auth_last_name': 'Пушкин', 'auth_middle_name': 'Сергеевич'},
    ]
}

BASE_DIR = os.path.dirname(__file__)
DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHOR_TABLE_NAME = 'authors'


exists_table_sql = f"""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name=?;
"""


@dataclass
class BookData:
    title: str
    author: 'AuthorData'
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class AuthorData:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: Dict[str, List]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            exists_table_sql,
            (BOOKS_TABLE_NAME,)
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_title TEXT NOT NULL,
                    auth_id INTEGER NOT NULL REFERENCES `books`(`auth_id`) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (book_title, auth_id) VALUES (?, ?)
                """,
                [
                    (item['book_title'], item['auth_id'])
                    for item in initial_records['books']
                ]
            )

            cursor.execute(
                f"""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='{AUTHOR_TABLE_NAME}';
                """
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.executescript(
                    f"""
                    CREATE TABLE `{AUTHOR_TABLE_NAME}`(
                        auth_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        auth_first_name TEXT NOT NULL,
                        auth_last_name TEXT NOT NULL,
                        auth_middle_name TEXT
                    );
                    """
                )
                cursor.executemany(
                    f"""
                    INSERT INTO `{AUTHOR_TABLE_NAME}`
                    (auth_first_name, auth_last_name, auth_middle_name)
                    VALUES (?, ?, ?)
                    """,
                    [
                        (item['auth_first_name'], item['auth_last_name'], item['auth_middle_name'])
                        for item in initial_records['authors']
                    ]
                )


def _get_book_obj_from_row(row: tuple) -> BookData:
    return BookData(id=row[0], title=row[1], author=get_author_by_id(row[2]))


def _get_author_obj_from_row(row: tuple) -> AuthorData:
    return AuthorData(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_all_books() -> list[BookData]:
    with sqlite3.connect(DATABASE_NAME, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: BookData) -> BookData:
    with sqlite3.connect(DATABASE_NAME, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (book_title, auth_id) VALUES (?, ?)
            """,
            (book.title, book.author.id)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[BookData]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE book_id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: BookData) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{BOOKS_TABLE_NAME}`
            SET book_title = ?, auth_id = ?
            WHERE book_id = ?
            """,
            (book.title, book.author.id, book.id)
        )
        conn.commit()


def delete_book_by_id(books_id: tuple | int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        if isinstance(books_id, tuple):
            books_id = str(books_id)[1:-1]
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM `{BOOKS_TABLE_NAME}`
            WHERE book_id IN ({books_id})
            """
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[BookData]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE book_title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_last_id_book() -> int:
    with sqlite3.connect(f'{BASE_DIR}/{DATABASE_NAME}') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""    
            SELECT MAX(book_id)
            FROM `{BOOKS_TABLE_NAME}`
            """
        )
        max_id = cursor.fetchone()
        return max_id[0]


def get_all_authors() -> list[AuthorData]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHOR_TABLE_NAME}`')
        all_authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_authors]


def get_author_by_id(auth_id: int):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHOR_TABLE_NAME}` WHERE auth_id = ?
            """,
            (auth_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_author_by_fullname(first_name: str, last_name: str, middle_name: str):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHOR_TABLE_NAME}`
            WHERE
                auth_first_name = ? AND
                auth_last_name = ? AND
                auth_middle_name = ?
            """,
            (first_name, last_name, middle_name)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def add_author(author: AuthorData) -> AuthorData:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHOR_TABLE_NAME}`
            (auth_first_name, auth_last_name, auth_middle_name)
            VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def get_all_author_books(auth_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE auth_id = ?
            """,
            (auth_id,)
        )
        books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in books]


def delete_auth_by_id(auth_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM `{AUTHOR_TABLE_NAME}`
            WHERE auth_id = ?
            """,
            (auth_id,)
        )
        conn.commit()
