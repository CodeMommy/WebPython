import re
import io
import importlib
import wsgiref.simple_server


class Dictionary:
    @staticmethod
    def http_status(status_name):
        status = dict()
        status[200] = "200 OK"
        status[404] = "404 Not Found"
        return status[status_name]

    @staticmethod
    def http_header(header_name):
        header = dict()
        header["content_plain"] = ("Content-type", "text/plain")
        return header[header_name]


class Server:
    def __int__(self):
        self.route = list()
        self.host = ""
        self.port = 8000
        self.controller_root = ""

    def start(self):
        application = Application(self.route, self.controller_root)
        server = wsgiref.simple_server.make_server(self.host, self.port, application)
        sock_name = server.socket.getsockname()
        self.welcome(sock_name)
        server.serve_forever()

    @staticmethod
    def welcome(sock_name):
        print("Welcome to use LuckyPython")
        print("Server Started At http://{0}:{1}/".format(*sock_name))


class Application:
    headers = list()

    def __init__(self, routes, controller_root):
        self.routes = routes
        self.controller_root = controller_root
        self.status = Dictionary.http_status(200)

    def __call__(self, environment, start_response):
        del self.headers[:]
        result = self.route(environment)
        start_response(self.status, self.headers)
        string_io = io.StringIO()
        if isinstance(result, str):
            print(result, file=string_io)
        else:
            pass
        return_list = list()
        return_list.append(string_io.getvalue().encode("utf-8"))
        return return_list

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))

    def route(self, environment):
        for method, pattern, name in self.routes:
            environment_method = environment["REQUEST_METHOD"]
            if environment_method.upper() == method.upper():
                environment_path = environment["PATH_INFO"]
                match = re.match('^' + pattern + '$', environment_path)
                if match:
                    names = name.split(".")
                    function_name = names.pop()
                    class_name = names.pop()
                    namespace_name = '.'.join(names)
                    namespace_name = "{0}.{1}".format(self.controller_root, namespace_name)
                    module_namespace = importlib.import_module(namespace_name)
                    if hasattr(module_namespace, class_name):
                        module_class = getattr(module_namespace, class_name)
                        if hasattr(module_class, function_name):
                            module_function = getattr(module_class, function_name)
                            args = match.groups()
                            return module_function(module_class, *args)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        return self.page404()

    def page404(self):
        self.status = Dictionary.http_status(404)
        self.header(*Dictionary.http_header("content_plain"))
        return "Not Found"


class View:
    def __init__(self, path):
        import jinja2
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        self.environment = environment

    def show_page(self, view, data):
        template = self.environment.get_template(view)
        return template.render(**data)
