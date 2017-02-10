""" CodeMommy WebPython About """

import abc


class About:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.vendor = 'CodeMommy'
        self.name = 'WebPython'
        self.version = '0.0.2'
        self.website = 'http://www.CodeMommy.com'
