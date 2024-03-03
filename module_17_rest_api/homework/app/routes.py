from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    init_db,
    get_all_books,
    get_book_by_id,
    add_book,
    update_book_by_id,
    delete_book_by_id,
    add_author,
    get_all_author_books,
    delete_auth_by_id
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookListResource(Resource):
    def get(self) -> tuple[list[dict] | str, int]:
        schema = BookSchema()
        books = get_all_books()
        if books:
            return schema.dump(books, many=True), 200
        return "", 404

    def post(self) -> tuple[dict, int]:
        data: dict = request.json

        if data.get('author', False):
            schema = BookSchema(exclude=['author_data'])
        else:
            schema = BookSchema(exclude=['author'])

        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BookResource(Resource):
    def get(self, book_id):
        schema = BookSchema()
        book = get_book_by_id(book_id)
        if book:
            return schema.dump(get_book_by_id(book_id))
        return "", 404

    def put(self, book_id):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book.id = book_id
        update_book_by_id(book)
        return '', 201

    def delete(self, book_id: int) -> tuple[str, int]:
        delete_book_by_id(book_id)
        return '', 204

    def patch(self, book_id):
        data = request.json
        schema = BookSchema()

        for key, value in schema.dump(get_book_by_id(book_id)).items():
            if key not in data and key != 'id':
                data[key] = value
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book.id = book_id
        update_book_by_id(book)
        return '', 201


class AuthorResource(Resource):
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    def get(self, auth_id):
        schema = BookSchema()
        books = get_all_author_books(auth_id)
        if books:
            return schema.dump(books, many=True)
        return "", 404

    def delete(self, auth_id):
        books = get_all_author_books(auth_id)
        books_id = tuple(book.id for book in books)
        if books_id:
            delete_book_by_id(books_id)
        delete_auth_by_id(auth_id)
        return '', 204


api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorResource, '/api/authors', '/api/authors/<int:auth_id>')


if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
