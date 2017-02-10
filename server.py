import WebPython
import application.config.route

if __name__ == "__main__":
    server = WebPython.Server()
    server.route = application.config.route.route
    server.controller_root = "application.controller"
    server.host = ""
    server.port = 80
    server.start()
else:
    pass
