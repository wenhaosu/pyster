import unittest


class FooTest(unittest.TestCase):
	def test_foo_func(self):
		foo = Foo()
		self.assertEquals(foo.foo_func(78595), 157190)
		self.assertEquals(foo.foo_func(699235148), 1398470296)
		self.assertEquals(foo.foo_func(412), 824)
		self.assertEquals(foo.foo_func(8133), 16266)
		self.assertEquals(foo.foo_func(4827), 9654)

	def test_get_info(self):
		foo = Foo()
		self.assertEquals(foo.get_info(), 'Foo Class')
		self.assertEquals(foo.get_info(), 'Foo Class')
		self.assertEquals(foo.get_info(), 'Foo Class')
		self.assertEquals(foo.get_info(), 'Foo Class')
		self.assertEquals(foo.get_info(), 'Foo Class')


if __name__ == "__main__":
	unittest.main()
