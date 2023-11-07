from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    print(request.form)
    return 'OK', 200


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, port=3000)
