import csv
import json
from datetime import date

from flask import Flask, jsonify, abort, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    init_db,
    Book,
    ReceivingBook,
    Author,
    recommendation_books_by_author_for_student,
    avg_number_books,
    get_popular_book,
    get_top_students,
    save_from_list_dicts,
)

from schemas import BookSchema, ReceivingBookSchema, StudentSchema, AuthorSchema


app = Flask(__name__)
api = Api(app)


class BookListResource(Resource):
    def get(self):
        schema = BookSchema()
        books = Book.get_all_books()
        if books:
            return schema.dump(books, many=True), 200
        return 'Книг в библиотеке пока нет', 200

    def post(self):
        schema = BookSchema()
        book_data: dict = request.json
        try:
            book = schema.load(book_data)
        except ValidationError as exc:
            return exc.messages, 400
        author_data = book.pop('author')
        author = Author(**author_data)
        author_loading = Author.get_author_by_id(name=author.name, surname=author.surname).scalar()

        if not author_loading:
            author = author.create_author(author)
        else:
            author = author_loading

        book = Book(**book)
        book.author_id = author.id
        if Book.get_book_by_authorid_and_name(author_id=book.author_id,
                                              name=book.name):
            return 'Такая книга уже есть в базе'
        book = Book.create_book(book)
        return schema.dump(book), 201


class ReceivingBookResource(Resource):
    def post(self):
        data = request.json
        schema = ReceivingBookSchema()
        try:
            receiving_book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        receiving_book = ReceivingBook.add_receiving_book(receiving_book)

        if receiving_book:
            print(receiving_book.count_date_with_book)
            return schema.dump(receiving_book), 201
        return 'На этом студенте уже числится данная книга', 400


class ReturnBookResource(Resource):
    def post(self):
        data = request.json
        schema = ReceivingBookSchema()
        try:
            receiving_book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        receiving_book = ReceivingBook.return_book(receiving_book)

        if receiving_book:
            print(receiving_book.count_date_with_book)
            return schema.dump(receiving_book), 201
        return 'На этом студенте не числится данная книга', 400


@app.route('/api/list_debtors', methods=['GET'])
def get_list_debtors():
    schema = StudentSchema()
    debtors = ReceivingBook.get_list_debtors()
    if debtors:
        return schema.dump(debtors, many=True), 200
    return 'Задолжников нет', 200


@app.route('/api/books/search', methods=['GET'])
def search_book():
    schema = BookSchema()
    search_str = request.args.get('search_str')
    books = Book.search_book(search_str)
    if books:
        return schema.dump(books, many=True)
    return 'Книги не найдены', 200


@app.route('/api/books/count_by_author', methods=['GET'])
def get_count_books_by_author():
    author_id = request.args.get('author_id')
    count_books = Book.get_count_books_by_author(author_id)
    return jsonify({'count': count_books})


@app.route('/api/recommendation_books', methods=['GET'])
def recommendation_books():
    student_id = request.args.get('student_id')
    schema = BookSchema()
    books = recommendation_books_by_author_for_student(student_id)
    return schema.dump(books, many=True)


@app.route('/api/avg_number_books', methods=['GET'])
def avg_number_books_month():
    avg_number = avg_number_books()
    return jsonify({'avg_number_books': avg_number})


@app.route('/api/popular_book', methods=['GET'])
def popular_book():
    schema = BookSchema()
    return schema.dump(get_popular_book())


@app.route('/api/top_students', methods=['GET'])
def top_students():
    schema = StudentSchema()
    return schema.dump(get_top_students(), many=True)


@app.route('/api/uploading_students_from_csv', methods=['POST'])
def uploading_students_from():
    file = request.files.get('file')
    file.save(file.filename)
    list_dicts_data = []
    with open(file.filename, newline='\n', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            row['scholarship'] = bool(row['scholarship'])
            row['average_score'] = float(row['average_score'])
            list_dicts_data.append(row)
    students = save_from_list_dicts(list_dicts_data)
    schema = StudentSchema()
    return schema.dump(students, many=True)


api.add_resource(BookListResource, '/api/books')
api.add_resource(ReceivingBookResource, '/api/receiving_books')
api.add_resource(ReturnBookResource, '/api/return_books')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
