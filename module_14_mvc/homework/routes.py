from flask import Flask, render_template, request
from typing import List
from wtforms import Form, StringField
from wtforms.validators import InputRequired
import flask_wtf

from models import init_db, get_all_books, DATA, added_book, get_books_by_author, get_book_info

app: Flask = Flask(__name__)


class AddedBooksForm(Form):
    book_title = StringField('Title', [InputRequired(message='Поле должно быть заполнено')])
    author_name = StringField('Author', [InputRequired(message='Поле должно быть заполнено')])


class SearchBooksForm(Form):
    author_name = StringField('Author', [InputRequired(message='Поле должно быть заполнено')])


@app.route('/books', methods=['GET', 'POST'])
def all_books() -> str:
    form = SearchBooksForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template(
            'books_by_author.html',
            books=get_books_by_author(form.author_name.data)
        )
    return render_template(
        'index.html',
        books=get_all_books(),
        form=form
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> str:
    form = AddedBooksForm(request.form)

    if request.method == 'POST' and form.validate():
        added_book(form.book_title.data, form.author_name.data)
        return render_template('index.html', books=get_all_books(), form=form)
    return render_template('add_book.html', form=form)


@app.route('/books/<string:author_name>', methods=['GET'])
def books_by_author(author_name) -> str:
    return render_template(
        'books_by_author.html',
        books=get_books_by_author(author_name)
    )


@app.route('/books/<int:book_id>', methods=['GET'])
def book_info(book_id):
    return render_template(
        'book_info.html',
        book=get_book_info(book_id)
    )


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
