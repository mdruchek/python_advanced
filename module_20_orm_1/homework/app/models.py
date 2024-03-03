import datetime
from datetime import date
from typing import List, Dict

from sqlalchemy import String, Integer, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy import select, insert, func, text, ColumnElement, case, distinct
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base: DeclarativeBase = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=1)
    release: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)

    @classmethod
    def get_all_books(cls):
        return session.execute(select(Book)).scalars().all()

    @classmethod
    def search_book(cls, search_str: str):
        return session.execute(select(Book).where(func.lower(Book.name).like(f'%{search_str}%'))).scalars().all()

    def __repr__(self) -> str:
        return (f"Book(id={self.id}, name={self.name}, count={self.count}, "
                f"release: {self.release}, author_id: {self.author_id})")


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name}, surname={self.surname})"


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, nullable=False)
    scholarship: Mapped[bool] = mapped_column(Boolean, nullable=False)

    @classmethod
    def get_students_receiving_scholarship(cls):
        return session.execute(select(Student).where(Student.scholarship)).scalars().all()

    @classmethod
    def get_students_by_average_score(cls, score):
        return session.execute(select(Student).where(Student.average_score > score)).scalars().all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_issue: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_of_return: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (f"ReceivingBook(id={self.id}, book_id={self.book_id}, student_id={self.student_id}, "
                f"date_of_issue={self.date_of_issue}, date_of_return={self.date_of_return})")

    @classmethod
    def add_receiving_book(cls, receiving_book):
        receiving_book_loading = session.execute(select(ReceivingBook)
                                                 .where(ReceivingBook.book_id == receiving_book.book_id,
                                                        ReceivingBook.student_id == receiving_book.student_id,
                                                        ReceivingBook.date_of_return.is_(None))).scalar_one_or_none()

        if not receiving_book_loading:
            book = session.get(Book, receiving_book.book_id)
            if book.count > 1:
                receiving_book.date_of_issue = datetime.datetime.now()
                book.count -= 1
                session.add(receiving_book)
                session.commit()
                return receiving_book

    @classmethod
    def return_book(cls, receiving_book):
        receiving_book = session.execute(select(ReceivingBook)
                                         .where(ReceivingBook.book_id == receiving_book.book_id,
                                                ReceivingBook.student_id == receiving_book.student_id,
                                                ReceivingBook.date_of_return.is_(None))).scalar_one_or_none()

        if receiving_book:
            book = session.get(Book, receiving_book.book_id)
            receiving_book.date_of_return = datetime.datetime.now()
            book.count += 1
            session.commit()

        return receiving_book

    @classmethod
    def get_list_debtors(cls):
        students_id = (session.execute(select(distinct(ReceivingBook.student_id))
                                      .where(ReceivingBook.date_of_return.is_(None))
                                      .filter(ReceivingBook.count_date_with_book > 14))
                       .scalars().all())

        if students_id:
            students = session.execute(select(Student).where(Student.id.in_(students_id))).scalars().all()
            return students

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        return (datetime.datetime.now() - self.date_of_issue).days

    @count_date_with_book.inplace.expression
    @classmethod
    def _count_date_with_book_expression(cls):
        return func.julianday(func.current_date()) - func.julianday(cls.date_of_issue)


DATA: dict = {
    'books': [
        Book(name='Война и Мир', count=10, release=date.today(), author_id=1),
        Book(name='Незнайка и его друзья', count=11, release=date.today(), author_id=2),
        Book(name='Капитанская дочка', count=12, release=date.today(), author_id=2),

    ],
    'authors': [
        Author(name='Лев', surname='Толстой'),
        Author(name='Николай', surname='Ноосов'),
        Author(name='Александр', surname='Пушкин'),
    ],
    'students': [
        Student(name='Иван', surname='Иванов', phone='1234567890', email='ivan@example.ru', average_score=5.0, scholarship=True),
        Student(name='Пётр', surname='Петров', phone='2345678901', email='petr@example.ru', average_score=4.0, scholarship=True),
        Student(name='Сидор', surname='Сидоров', phone='3456789012', email='sidor@example.ru', average_score=3.0, scholarship=False),
    ]
}


def init_db(initial_record: Dict[str, List]) -> None:
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for list_obj in initial_record.values():
        session.add_all(list_obj)
    session.commit()
