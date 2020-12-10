from .too import Too


def dummy():
    print("Dummy!")


class Baz(object):
    def __init__(self, t: Too):
        self.t = t

    def method(self, x):
        return x
