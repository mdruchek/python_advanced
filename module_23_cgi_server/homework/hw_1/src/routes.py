import json
import re


class Application:
    def __init__(self, name):
        self.name = name
        self.route = {}

    def __call__(self, *args):
        if isinstance(args[0], str):
            def wrapper(func):
                url_args: str = args[0]
                url_args = re.split(r'<.*>', url_args)[0]
                self.route[url_args] = func
            return wrapper
        if isinstance(args[0], dict):
            env = args[0]
            start_response = args[1]
            url: str = env.get('REQUEST_URI')
            url_list = re.split(r'(\/hello\/)', url)
            url_list = list(filter(lambda x: x != '', url_list))
            url = url_list[0]
            if url in self.route and ((url.endswith('/') and len(url_list) == 2) or not url.endswith('/')):
                route = self.route.get(url)
                if url.endswith('/'):
                    name = url_list[1]
                    response = route(name)
                else:
                    response = route()
                start_response('200 OK', [('Content-Type', 'text/html')])
                return response
            start_response('404 Page not found', [('Content-Type', 'text/html')])
            return json.dumps({"error": "page not found"}, indent=4).encode('utf-8')


application = Application(__name__)


@application('/hello')
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4).encode('utf-8')


@application('/hello/<name>')
def say_hello_name(name):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4).encode('utf-8')
