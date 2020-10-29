import unittest
from foobar import Foo


class FooTest(unittest.TestCase):
	def test_foo_func(self):
		foo = Foo()
		self.assertEqual(foo.foo_func(3), 6)
		self.assertEqual(foo.foo_func(52696876), 105393752)
		self.assertEqual(foo.foo_func(198), 396)
		self.assertEqual(foo.foo_func(64), 128)
		self.assertEqual(foo.foo_func(36929), 73858)

	def test_get_info(self):
		foo = Foo()
		self.assertEqual(foo.get_info(), 'Foo Class')
		self.assertEqual(foo.get_info(), 'Foo Class')
		self.assertEqual(foo.get_info(), 'Foo Class')
		self.assertEqual(foo.get_info(), 'Foo Class')
		self.assertEqual(foo.get_info(), 'Foo Class')


if __name__ == "__main__":
	unittest.main()
