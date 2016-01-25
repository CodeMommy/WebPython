import re
import io
import importlib
import wsgiref.simple_server
import routes


class Server:
    @staticmethod
    def start(host="", port=8000):
        print("Welcome to use LuckyPython")
        httpd = wsgiref.simple_server.make_server(host, port, Application())
        sa = httpd.socket.getsockname()
        print("Server Started At http://{0}:{1}/".format(*sa))
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

    def __init__(self):
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
        environment_path = environment["PATH_INFO"]
        environment_method = environment["REQUEST_METHOD"]
        for method, pattern, name in routes.routes:
            if environment_method.upper() == method.upper():
                names = name.split(".")
                function_name = names.pop()
                class_name = names.pop()
                namespace_name = '.'.join(names)
                match = re.match('^' + pattern + '$', environment_path)
                if match:
                    args = match.groups()
                    namespace = "application.controller.{0}".format(namespace_name)
                    module_namespace = importlib.import_module(namespace)
                    if hasattr(module_namespace, class_name):
                        module_class = getattr(module_namespace, class_name)
                        if hasattr(module_class, function_name):
                            module_function = getattr(module_class, function_name)
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
