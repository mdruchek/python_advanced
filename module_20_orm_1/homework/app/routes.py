from datetime import date

from flask import Flask, jsonify, abort, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import DATA, init_db, Book, ReceivingBook
from schemas import BookSchema, ReceivingBookSchema, StudentSchema


app = Flask(__name__)
api = Api(app)


class BookListResource(Resource):
    def get(self):
        schema = BookSchema()
        books = Book.get_all_books()
        if books:
            return schema.dump(books, many=True), 200
        return 'Книг в библиотеке пока нет', 200


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


api.add_resource(BookListResource, '/api/books')
api.add_resource(ReceivingBookResource, '/api/receiving_books')
api.add_resource(ReturnBookResource, '/api/return_books')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
