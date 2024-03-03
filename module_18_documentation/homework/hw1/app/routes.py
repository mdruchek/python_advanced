import json
import logging

from flask import Flask, request

from flask_restful import Api, Resource
from marshmallow import ValidationError

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import swag_from, APISpec, Swagger

from werkzeug.serving import WSGIRequestHandler

from models import (
    BookData,
    DATA,
    init_db,
    get_all_books,
    get_book_by_id,
    add_book,
    update_book_by_id,
    delete_book_by_id,
    get_all_authors,
    add_author,
    get_author_by_fullname,
    get_author_by_id,
    get_all_author_books,
    delete_auth_by_id,
    BASE_DIR
)

from schemas import BookSchema, AuthorSchema

logger = logging.getLogger()
logger.disabled = True

app = Flask(__name__)
api = Api(app)

spec = APISpec(
    title='Library of books',
    version='1.0.0',
    openapi_version='3.1',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin()

    ]
)


def my_swag_from(func):
    def wrapper(*args, **kwargs):
        with open(args[0]) as file:
            f = func(json.load(file))
        return f
    return wrapper


new_swag_from = my_swag_from(swag_from)


class BookListResource(Resource):
    @swag_from('../documentations/books_get.yml')
    def get(self) -> tuple[list[dict] | str, int]:
        schema = BookSchema()
        books = get_all_books()

        if books:
            return schema.dump(books, many=True), 200
        return "", 404

    @swag_from('../documentations/books_post.yml')
    def post(self) -> tuple[dict, int]:
        data: dict = request.json

        schema = BookSchema()
        schema.context['method'] = request.method
        schema.context['schema'] = 'Book'

        try:
            book: BookData = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = get_author_by_fullname(
            first_name=book.author.first_name,
            last_name=book.author.last_name,
            middle_name=book.author.middle_name
        )
        if not author:
            author = add_author(book.author)

        book.author = author
        book = add_book(book)
        return schema.dump(book), 201


class BookResource(Resource):
    @swag_from('../documentations/book_id_get.yml')
    def get(self, book_id):
        schema = BookSchema()
        book = get_book_by_id(book_id)

        if book:
            return schema.dump(book)
        return "", 404

    @swag_from('../documentations/book_id_put.yml')
    def put(self, book_id):

        if get_book_by_id(book_id) is None:
            return "", 404

        data = request.json
        schema = BookSchema()
        schema.context['book_id'] = book_id
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book.id = book_id

        author = get_author_by_fullname(
            first_name=book.author.first_name,
            last_name=book.author.last_name,
            middle_name=book.author.middle_name
        )

        if not author:
            author = add_author(book.author)

        book.author = author
        update_book_by_id(book)
        return schema.dump(book), 201

    @swag_from('../documentations/book_id_del.yml')
    def delete(self, book_id: int) -> tuple[str, int]:

        if get_book_by_id(book_id) is None:
            return '', 404

        delete_book_by_id(book_id)
        return '', 204

    @swag_from('../documentations/book_id_patch.yml')
    def patch(self, book_id):

        if get_book_by_id(book_id) is None:
            return "", 404

        data: dict = request.json
        schema = BookSchema()
        schema.context['book_id'] = book_id

        for key, value in schema.dump(get_book_by_id(book_id)).items():
            if key not in data and key != 'id':
                data[key] = value

        data.get('author').pop('id')

        try:
            book: BookData = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book.id = book_id

        author = get_author_by_fullname(
            first_name=book.author.first_name,
            last_name=book.author.last_name,
            middle_name=book.author.middle_name
        )

        if not author:
            author = add_author(book.author)

        book.author = author

        update_book_by_id(book)
        return schema.dump(book), 201


class AuthorListResource(Resource):
    @new_swag_from('../documentations/authors_get.json')
    def get(self) -> tuple[list[dict] | str, int]:
        schema = AuthorSchema()
        authors = get_all_authors()

        if authors:
            return schema.dump(authors, many=True), 200
        return "", 404

    @new_swag_from('../documentations/authors_post.json')
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        schema.context['method'] = request.method
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


class AuthorResource(Resource):
    @new_swag_from('../documentations/author_id_get.json')
    def get(self, auth_id):
        schema = BookSchema()
        books = get_all_author_books(auth_id)
        if books:
            return schema.dump(books, many=True)
        return "", 404

    @new_swag_from('../documentations/author_id_del.json')
    def delete(self, auth_id):

        if get_author_by_id(auth_id) is None:
            return "", 404

        books = get_all_author_books(auth_id)
        books_id = tuple(book.id for book in books)
        if books_id:
            delete_book_by_id(books_id)
        delete_auth_by_id(auth_id)
        return '', 204


template = spec.to_flasgger(
    app,
    definitions=[BookSchema]
)

swagger = Swagger(app, template=template)

api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorListResource, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:auth_id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
