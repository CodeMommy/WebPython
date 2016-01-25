import LuckyPython
import application.configuration.route

if __name__ == "__main__":
    server = LuckyPython.Server()
    server.route = application.configuration.route.route
    server.controller_root = "application.controller"
    server.host = ""
    server.port = 8000
    server.start()
