# Sample Python program including two simple classes
from typing import List
from .baz import Baz


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


def main():
    foo = Foo('Foo Class')
    bar = Bar()
    print(foo.foo_func(16))
    print(bar.bar_func(16))


if __name__ == "__main__":
    main()
