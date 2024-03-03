from flask import Flask, render_template
from typing import List

from models import init_db, get_all_books, DATA, get_filter_books, get_total_number_books

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
        number=get_total_number_books()
    )


@app.route('/books/form')
def get_books_form() -> str:
    return render_template('add_book.html')


@app.route('/books/<string:author>')
def search_books(author: str):
    return render_template(
        'index.html',
        books=get_filter_books(author)
    )


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
