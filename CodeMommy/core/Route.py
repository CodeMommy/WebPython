import io
import re
import abc
import importlib
import CodeMommy.core.Http


class Route:
    __metaclass__ = abc.ABCMeta
    headers = list()

    def __init__(self, routes, controller_root):
        self.routes = routes
        self.controller_root = controller_root
        self.status = CodeMommy.core.Http.Http.status(200)
        self.header(*CodeMommy.core.Http.Http.header("content_plain"))

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
                match = re.match("^" + pattern + "$", environment_path)
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
                            getattr(module_class, "__init__")(module_class, *args)
                            self.status = CodeMommy.core.Http.Http.status(200)
                            return module_function(module_class, *args)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        self.status = CodeMommy.core.Http.Http.status(404)
        return self.status
