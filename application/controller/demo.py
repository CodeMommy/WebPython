import CodeMommy.WebPython


class Demo:
    def __init__(self):
        self.output = CodeMommy.WebPython.Output("application/view")

    def welcome(self):
        data = dict()
        data["name"] = "World"
        return self.output.template("demo/welcome.html", data)
