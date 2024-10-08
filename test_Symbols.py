import unittest
from parameterized import parameterized
from Symbols import Symbols


class Test_XML_Keys(unittest.TestCase):
    @parameterized.expand([
        ("Gained Arrow", Symbols.GAINED, u'\u2B9D'),
        ("Lost Arrow", Symbols.LOST, u'\u2B9F'),
    ])
    def test_symbols(self, name, input, expected):
        self.assertEqual(input, expected)


if __name__ == '__main__':
    unittest.main()
