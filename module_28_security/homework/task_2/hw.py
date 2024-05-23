from flask import Flask, jsonify, request, Response

page_header = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
      <meta charset="UTF-8">
      <title>Title</title>
    </head>

    <body>
      <form action="" method="GET">
"""

page_footer = """
      </form>
    </body>

    </html>
"""

main_page_markup = """
    <form action="" method="GET">
      <input id="query" name="query" value="Enter query here..."
        onfocus="this.value=''">
      <input id="button" type="submit" value="Search">
    </form>
"""

app = Flask(__name__)


@app.route('/xss', methods=['GET'])
def xss():
    if not request.args.get('query'):
        input = main_page_markup
    else:
        input = request.args.get('query')
    return page_header + input + page_footer


@app.after_request
def add_cors(response: Response):
    response.headers['Content-Security-Policy'] = 'default-src "self"'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)

