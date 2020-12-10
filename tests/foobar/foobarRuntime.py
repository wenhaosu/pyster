import foobar.foobar
import foobar
import foobar.baz
import foobar.too


def test_init_Bar():
    var = foobar.foobar.Bar()
    ret = var
    assert isinstance(ret, foobar.foobar.Bar)


def test_bar_func_Bar():
    var = foobar.foobar.Bar()
    ret = var.bar_func(3003713024)
    assert ret is not None


def main():
    test_init_Bar()
    test_bar_func_Bar()
