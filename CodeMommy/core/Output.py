import abc
import jinja2


class Output:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.environment = None
        self.set_path(path)

    def set_path(self, path):
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        self.environment = environment

    def template(self, template, data):
        template = self.environment.get_template(template)
        return template.render(**data)
