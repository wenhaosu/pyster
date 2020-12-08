# Sample Python program including two simple classes
from typing import List
from .baz import Baz


def hello_world():
    print("Hello World!")


def positive_num(num: int):
    if num <= 0:
        return False
    return True


class Foo:
    def __init__(self, info: str):
        self.res = 0
        self.info = info

    def foo_func(self, x: int = 2) -> int:
        self.res = x * 2
        return self.res

    def get_info(self) -> str:
        return self.info

    def call_baz(self, x: Baz):
        pass

    def raise_exception(self):
        raise NotImplementedError


class Bar:
    def __init__(self):
        self.res = 0
        self.info = "Bar Class"
        self.array = []

    def bar_func(self, x: int = 2) -> float:
        self.res = x / 2
        return self.res

    def get_info(self) -> str:
        return self.info

    def call_bar_obj(self, obj: Foo) -> str:
        return self.get_info() + " has a " + obj.get_info()

    def set_array(self, arr: List[bool] = [True, False]):
        self.array = arr
