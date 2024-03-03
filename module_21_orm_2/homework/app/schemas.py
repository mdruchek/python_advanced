from marshmallow import (
    Schema,
    fields,
    post_load,
)

from models import (
    Author,
    Book,
    ReceivingBook,
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)

    # @post_load
    # def create_author(self, data: dict, **kwargs):
    #     author = Author(**data)
    #     return author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    count = fields.Int()
    release = fields.Date(required=True)
    author = fields.Nested(AuthorSchema)

    # @post_load
    # def create_book(self, data: dict, **kwargs):
    #     book = Book(**data)
    #     return book


class ReceivingBookSchema(Schema):
    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    date_of_issue = fields.Date()
    date_of_return = fields.Date()

    @post_load
    def create_receiving_book(self, data: dict, **kwargs):
        rec_book = ReceivingBook(**data)
        return rec_book


class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str(required=True)
    average_score = fields.Float(required=True)
    scholarship = fields.Bool(required=True)
