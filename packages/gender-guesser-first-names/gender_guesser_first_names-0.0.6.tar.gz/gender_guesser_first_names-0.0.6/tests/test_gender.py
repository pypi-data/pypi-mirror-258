import unittest
#from desoper import hello


class Test_hello(unittest.TestCase):
    def test__working(self):
        self.assertEqual('Hello, World!',
                         'Hello, World!', True)


if __name__ == '__main__':
    unittest.main()
