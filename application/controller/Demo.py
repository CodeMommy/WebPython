import LuckyPython


class Demo:
    @staticmethod
    def welcome(self):
        data = dict()
        data["name"] = "World"
        view = LuckyPython.View("application/view")
        return view.show_page("Demo/welcome.html", data)

    @staticmethod
    def hello(self, name):
        return "Hello {0}!".format(name)
