from typing import Any, Optional, List, NoReturn

import sqlite3


class Room:
    def __init__(
            self,
            id: int,
            floor: int,
            beds: int,
            guest_num: int,
            price: int,
            check_in: Optional[str] = None,
            check_out: Optional[str] = None,
            firstname: Optional[str] = None,
            lastname: Optional[str] = None
    ):
        self.id: int = id
        self.floor: int = floor
        self.beds: int = beds
        self.guest_num: int = guest_num
        self.price: int = price
        self.check_in: str = check_in
        self. check_out: str = check_out
        self.firstname: str = firstname
        self.lastname: str = lastname

    def __getitem__(self, item) -> Any:
        return getattr(self, item)


def init_db() -> None:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT `name` FROM `sqlite_master`
            """
        )
        exists: Optional[tuple[str]] = cursor.fetchone()
        if not exists:
            cursor.execute(
                """
                CREATE TABLE `rooms` (
                    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                    `floor` INT,
                    `beds` INT,
                    `guest_num` INT,
                    `price` INT,
                    `check_in` DATE,
                    `check_out` DATE,
                    `firstname` TEXT,
                    `lastname` TEXT
                )
                """
            )


insert_room_sql = """
    INSERT INTO `rooms`
        (floor, beds, guest_num, price)
        VALUES
        (?, ?, ?, ?);
"""

get_all_rooms_sql = """
    SELECT *
        FROM `rooms`;
"""

get_rooms_sql = """
    SELECT *
        FROM `rooms`
        WHERE `guest_num` = ? AND
                (((`check_in` NOT BETWEEN ? AND ?) AND
                (`check_out` NOT BETWEEN ? AND ?)) OR 
                (`check_in` IS NULL AND `check_out` IS NULL ));
"""

get_room_sql = """
    SELECT *
        FROM `rooms`
        WHERE id = ?
"""

update_room_sql = """
    UPDATE `rooms`
        SET `check_in` = ?,
            `check_out` = ?,
            `firstname` = ?,
            `lastname` = ?
        WHERE id = ?
"""


def insert_room(floor: int, beds: int, guest_num: int, price: int) -> None:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            insert_room_sql,
            (floor, beds, guest_num, price)
        )


def get_all_rooms() -> List[Room]:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            get_all_rooms_sql
        )
        rooms: List = cursor.fetchall()
        return [Room(*room_arg) for room_arg in rooms]


def get_rooms(guest_num: int, check_in: str, check_out: str) -> List[Room]:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            get_rooms_sql,
            (guest_num, check_in, check_out, check_in, check_out)
        )
        rooms: List = cursor.fetchall()
        return [Room(*room_arg) for room_arg in rooms]


def get_room_from_db(room_id: int) -> Room:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            get_room_sql,
            (room_id,)
        )
        room_arg: tuple = cursor.fetchone()
        return Room(*room_arg)


def update_room(check_in, check_out, firstname, lastname, room_id) -> None:
    with sqlite3.connect('hotels.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            update_room_sql,
            (check_in, check_out, firstname, lastname, room_id)
        )
