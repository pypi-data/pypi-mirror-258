import unittest
from sdle_empty_package.sdle_empty_module import say_hello


class SdleEmptyModule(unittest.TestCase):
    def test_say_hello(self):
        self.assertEqual(say_hello(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
