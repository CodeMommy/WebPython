import re
import io
import importlib
import wsgiref.simple_server


class Server:
    def __int__(self):
        self.route = list()
        self.host = ""
        self.port = 8000
        self.controller_root = ""

    def start(self):
        print("Welcome to use LuckyPython")
        application = Application(self.route, self.controller_root)
        httpd = wsgiref.simple_server.make_server(self.host, self.port, application)
        sock_name = httpd.socket.getsockname()
        print("Server Started At http://{0}:{1}/".format(*sock_name))
        httpd.serve_forever()


class Application:
    headers = list()

    @staticmethod
    def response_status(status_name):
        status = dict()
        status[200] = "200 OK"
        status[404] = "404 Not Found"
        return status[status_name]

    @staticmethod
    def response_header(header_name):
        header = dict()
        header["content_plain"] = ("Content-type", "text/plain")
        return header[header_name]

    def __init__(self, routes, controller_root):
        self.routes = routes
        self.controller_root = controller_root
        self.status = self.response_status(200)

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

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))

    def page404(self):
        self.status = self.response_status(404)
        self.header(*self.response_header("content_plain"))
        return "Not Found"
