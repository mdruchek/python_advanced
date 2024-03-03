from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError,
    post_load
)

from models import (
    get_book_by_title,
    get_author_by_id,
    get_author_by_fullname,
    BookData,
    AuthorData,
    add_author
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

    @validates_schema()
    def validate_auth_fullname(self, data, **kwargs):
        author = get_author_by_fullname(**data)
        if author is not None:
            auth_full_name = f'{author.last_name} {author.first_name} {author.middle_name}'
            raise ValidationError(
                'Автор {fullname} уже есть в базе, '
                'с id={auth_id}'.format(fullname=auth_full_name, auth_id=author.id)
            )

    @post_load
    def create_author(self, data: dict, **kwargs) -> AuthorData:
        author = AuthorData(**data)
        return author


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Int(required=True)
    author_data = fields.Nested(AuthorSchema, required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Книга с названием "{title}" уже существует, '
                'используйте другое название.'.format(title=title)
            )

    @validates('author')
    def validate_author(self, auth_id: int):
        if get_author_by_id(auth_id) is None:
            raise ValidationError(
                'Автора с id {id} не найден в базе данных, '
                'сначало создайте автора'.format(id=auth_id)
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> BookData:
        author_data: AuthorData | bool = data.pop('author_data', False)
        if author_data:
            author = add_author(author_data)
            data['author'] = author.id
        book = BookData(**data)
        return book

