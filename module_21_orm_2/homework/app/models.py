import datetime
import calendar
import re
import statistics
from datetime import date
from typing import List, Dict

from sqlalchemy.engine import Engine
from sqlalchemy import String, Integer, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy import select, insert, update, func, text, ColumnElement, case, distinct, desc
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy


engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base: DeclarativeBase = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(default=1)
    release: Mapped[date] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)

    author: Mapped['Author'] = relationship(back_populates='books', lazy='joined')
    students: Mapped[List['ReceivingBook']] = relationship(back_populates='book', lazy='subquery', passive_deletes=True)

    @classmethod
    def get_all_books(cls):
        return session.execute(select(Book)).unique().scalars().all()

    @classmethod
    def create_book(cls, book):
        session.add(book)
        session.commit()
        return book

    @classmethod
    def search_book(cls, search_str: str):
        return session.execute(select(Book).where(func.lower(Book.name).like(f'%{search_str}%'))).scalars().all()

    @classmethod
    def get_count_books_by_author(cls, author_id):
        return session.execute(select(func.sum(Book.count)).where(Book.author_id == author_id)).scalar()

    @classmethod
    def get_book_by_authorid_and_name(cls, author_id, name):
        return session.execute(select(Book)
                               .where(Book.author_id == author_id)
                               .where(Book.name == name)).scalar()

    def __repr__(self) -> str:
        return (f"Book(id={self.id}, name={self.name}, count={self.count}, "
                f"release: {self.release}, author_id: {self.author_id})")


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    books: Mapped[List['Book']] = relationship(back_populates='author', cascade='all, delete-orphan',
                                               lazy='joined', passive_deletes=True)

    @classmethod
    def get_author_by_id(cls, name, surname):
        return session.execute(select(Author)
                               .where(Author.name == name)
                               .where(Author.surname == surname))

    @classmethod
    def create_author(cls, author):
        session.add(author)
        session.commit()
        return author

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name}, surname={self.surname})"


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    average_score: Mapped[float] = mapped_column(nullable=False)
    scholarship: Mapped[bool] = mapped_column(nullable=False)

    books: Mapped[List['ReceivingBook']] = relationship(back_populates='student', lazy='subquery', passive_deletes=True)

    keywords: AssociationProxy[List[Book]] = association_proxy(
        'books',
        "students",
        creator=lambda book_obj: ReceivingBook(books=book_obj),
    )

    @classmethod
    def get_students_receiving_scholarship(cls):
        return session.execute(select(Student).where(Student.scholarship)).scalars().all()

    @classmethod
    def get_students_by_average_score(cls, score):
        return session.execute(select(Student).where(Student.average_score > score)).scalars().all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'))
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    date_of_issue: Mapped[date] = mapped_column(default=date.today(), nullable=False)
    date_of_return: Mapped[date] = mapped_column(nullable=True)

    book: Mapped['Book'] = relationship(back_populates='students', lazy='selectin')
    student: Mapped['Student'] = relationship(back_populates='books', lazy='selectin')

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
            receiving_book.date_of_return = datetime.date.today()
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
        return (datetime.date.today() - self.date_of_issue).days

    @count_date_with_book.inplace.expression
    @classmethod
    def _count_date_with_book_expression(cls):
        return func.julianday(func.current_date()) - func.julianday(cls.date_of_issue)


def recommendation_books_by_author_for_student(student_id):
    book_id_sub = select(ReceivingBook.book_id).where(ReceivingBook.student_id == student_id)
    authors_id_sub = select(Book.author_id).distinct().where(Book.id.in_(book_id_sub))
    books = (session.execute(select(Book)
                             .where(Book.author_id.in_(authors_id_sub))
                             .where(Book.id.not_in(book_id_sub))).unique().scalars().all())
    return books


def avg_number_books():
    date_today = date.today()
    days_in_month = calendar.monthrange(date_today.year, date_today.month)[1]
    count_books_by_students = session.execute(select(func.count(ReceivingBook.book_id))
                                              .where(ReceivingBook.date_of_issue.between(date_today.replace(day=1),
                                                                                         date_today.replace(day=1) + datetime.timedelta(days=days_in_month)))
                                              .group_by(ReceivingBook.student_id)).scalars().all()
    return statistics.mean(count_books_by_students)


def get_popular_book():
    book = session.execute(select(Book)
                           .join(ReceivingBook)
                           .join(Student)
                           .where(Student.average_score > 4.0)
                           .group_by(ReceivingBook.book_id)
                           .order_by(desc(func.count(Book.id)))
                           .limit(1)).scalar()
    return book


def get_top_students():
    students = session.execute(select(Student)
                               .join(ReceivingBook)
                               .group_by(ReceivingBook.student_id)
                               .order_by(desc(func.count(ReceivingBook.student_id)))
                               .limit(10)).scalars().all()
    return students


def save_from_list_dicts(data):
    students = session.scalars(insert(Student).returning(Student), data)
    session.commit()
    return students


@event.listens_for(Student.phone, 'set')
def receive_set(target, value, oldvalue, initiator):
    if not re.match(r'\+7\(9[0-9]{2}\)-[0-9]{3}-[0-9]{2}-[0-9]{2}', value, flags=0):
        raise ValueError

DATA = {
    'books': [
        {'name': 'Война и Мир', 'count': 10, 'release': date.today(), 'author_id': 1},
        {'name': 'Незнайка и его друзья', 'count': 11, 'release': date.today(), 'author_id': 2},
        {'name': 'Капитанская дочка', 'count': 12, 'release': date.today(), 'author_id': 3},
    ],
    'authors': [
        {'name': 'Лев', 'surname': 'Толстой'},
        {'name': 'Николай', 'surname': 'Носов'},
        {'name': 'Александр', 'surname': 'Пушкин'},
    ],
    'students': [
        {'name': 'Иван', 'surname': 'Иванов', 'phone': '1234567890',
         'email': 'ivan@example.ru', 'average_score': 5.0, 'scholarship': True},
        {'name': 'Пётр', 'surname': 'Петров', 'phone': '2345678901',
         'email': 'petr@example.ru', 'average_score': 4.0, 'scholarship': True},
        {'name': 'Сидор', 'surname': 'Сидоров', 'phone': '3456789012',
         'email': 'sidor@example.ru', 'average_score': 3.0, 'scholarship': False},
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

    for class_, dict_ in zip([Author, Book, Student],
                             [initial_record['authors'], initial_record['books'], initial_record['students']]):

        session.bulk_insert_mappings(class_, dict_)
    session.commit()
