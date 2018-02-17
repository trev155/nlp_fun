import unittest
import main.preprocessing_helpers


class TestSeparateCSVLine(unittest.TestCase):
    def test_simple(self):
        s = 'hello,world,123,456'
        expected = ['hello', 'world', '123', '456']
        actual = main.preprocessing_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)

    def test_complex(self):
        s = '"hello,world",123,456,789'
        expected = ['hello,world', '123', '456', '789']
        actual = main.preprocessing_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)

    def test_complex_multiple(self):
        s = '"hi,hey",123,"ha,hi,he",456'
        expected = ['hi,hey', '123', 'ha,hi,he', '456']
        actual = main.preprocessing_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
