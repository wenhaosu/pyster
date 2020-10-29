# Sample Python program including two simple classes

class Foo:
    def __init__(self, info: str):
        self.res = 0
        self.info = info

    def foo_func(self, x: int = 2) -> int:
        self.res = x * 2
        return self.res

    def get_info(self) -> str:
        return self.info


class Bar:
    def __init__(self):
        self.res = 0
        self.info = "Bar Class"

    def bar_func(self, x: int) -> float:
        self.res = x / 2
        return self.res

    def get_info(self) -> str:
        return self.info

    # def call_bar_obj(self, obj: Foo) -> str:
    #     return self.get_info() + " has a " + obj.get_info()


def main():
    foo = Foo('Foo Class')
    bar = Bar()
    print(foo.foo_func(16))
    print(bar.bar_func(16))


if __name__ == "__main__":
    main()
