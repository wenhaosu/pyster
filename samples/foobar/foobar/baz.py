from .too import Too


class Baz(object):
    def __init__(self, t: Too):
        self.t = t

    def method(self, x):
        return x
