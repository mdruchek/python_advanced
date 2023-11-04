import logging
import flask

from http_utils import get_ip_address
from subprocess_utils import get_kernel_version


root_loger = logging.getLogger()
logging.basicConfig()
logger_main = logging.getLogger('main')
logger_utils = logging.getLogger('utils')
logger_main.setLevel('INFO')
logger_utils.setLevel('DEBUG')


app = flask.Flask(__name__)


@app.route('/get_system_info')
def get_system_info():
    logger_main.info('Start working')
    ip = get_ip_address()
    kernel = get_kernel_version()
    return "<p>{}</p><p>{}</p>".format(ip, kernel)


if __name__ == '__main__':
    print(logger_main.parent)
    print(logger_utils.parent.handlers)
    print(logger_main.handlers)
    print(logger_utils.handlers)
    app.run(debug=True)
