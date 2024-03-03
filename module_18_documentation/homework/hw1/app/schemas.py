from flasgger import Schema, fields, ValidationError
from marshmallow import (
    validates,
    validates_schema,
    post_load
)

from models import (
    get_book_by_title,
    BookData,
    AuthorData,
    get_author_by_fullname,
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

    @validates_schema()
    def validate_fullname(self, data, **kwargs) -> None:
        author: AuthorData = get_author_by_fullname(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name']
        )

        if author is not None and self.context.get('method') == 'POST' and self.context.get('schema') != 'Book':
            raise ValidationError(
                'Автор {last_name} {first_name} {middle_name}'
                'уже есть в базе под номером {auth_id}'
                .format(
                    last_name=data['last_name'],
                    first_name=data['first_name'],
                    middle_name=data['middle_name'],
                    auth_id=author.id
                )
            )

    @post_load
    def create_author(self, data: dict, **kwargs) -> AuthorData:
        author = AuthorData(**data)
        return author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Nested(AuthorSchema)

    @validates('title')
    def validate_title(self, title: str) -> None:
        book = get_book_by_title(title)
        if book is not None and (self.context.get('method') == 'POST' or self.context.get('book_id') != book.id):
            raise ValidationError(
                'Книга с названием "{title}" уже существует, '
                'используйте другое название.'.format(title=title)
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> BookData:
        book = BookData(**data)
        return book

