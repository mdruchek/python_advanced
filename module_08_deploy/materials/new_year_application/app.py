import os

from flask import Flask, render_template, send_from_directory, url_for

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(template_folder, "static")
js_directory = os.path.join(static_directory, "js")
css_directory = os.path.join(static_directory, "css")
images_directory = os.path.join(static_directory, "images")
static_directories = {
    'js': js_directory,
    'css': css_directory,
    'images': images_directory
}
app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:directory>/<path:path>")
def send_static(directory, path):
    return send_from_directory(directory=static_directories[directory], path=path)


if __name__ == "__main__":
    app.run()
