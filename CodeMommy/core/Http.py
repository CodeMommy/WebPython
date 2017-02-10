import abc


class Http:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def status(status_name):
        status = dict()
        status[200] = "200 OK"
        status[404] = "404 Not Found"
        return status[status_name]

    @staticmethod
    def header(header_name):
        header = dict()
        header["content_plain"] = ("Content-type", "text/plain;charset=utf-8")
        return header[header_name]
