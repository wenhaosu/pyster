# Sample Python program including two simple classes

class Foo:
    def foo_func(self, x):
        return x * 2

    def get_info(self):
        return "Foo Class"

class Bar:
    def bar_func(self, x):
        return x / 2

    def get_info(self):
        return "Bar Class"

def main():
    foo = Foo()
    bar = Bar()
    print(foo.foo_func(16))
    print(bar.bar_func(16))

if __name__ == "__main__":
    main()
