import abc
import time
import wsgiref.simple_server
import CodeMommy


class Server:
    __metaclass__ = abc.ABCMeta

    def __int__(self):
        self.route = list()
        self.host = ""
        self.port = 80
        self.controller_root = ""

    def start(self):
        route = CodeMommy.core.Route.Route(self.route, self.controller_root)
        server = wsgiref.simple_server.make_server(self.host, self.port, route)
        sock_name = server.socket.getsockname()
        self.welcome(sock_name)
        server.serve_forever()

    @staticmethod
    def welcome(sock_name):
        time_now = time.strftime("%Y-%m-%d %X", time.localtime())
        about = CodeMommy.core.About.About()
        line = "-------------------------------------------------------------"
        print(line)
        print("Welcome to use {0} {1} by {2}".format(about.name, about.version, about.vendor))
        print("Get more information please visit {0}".format(about.website))
        print(line)
        print("{0} - Server Started At http://{1}:{2}/".format(time_now, *sock_name))
        print(line)
