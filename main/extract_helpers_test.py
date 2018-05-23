import unittest
import extract_helpers


class TestSeparateCSVLine(unittest.TestCase):
    def test_simple(self):
        s = 'hello,world,123,456'
        expected = ['hello', 'world', '123', '456']
        actual = extract_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)

    def test_complex(self):
        s = '"hello,world",123,456,789'
        expected = ['hello,world', '123', '456', '789']
        actual = extract_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)

    def test_complex_multiple(self):
        s = '"hi,hey",123,"ha,hi,he",456'
        expected = ['hi,hey', '123', 'ha,hi,he', '456']
        actual = extract_helpers.separate_csv_line(s)
        self.assertEqual(expected, actual)


class TestPreprocessingString(unittest.TestCase):
    def test_remove_whitespace(self):
        s = "      hello world "
        expected = "hello world"
        actual = extract_helpers.remove_whitespace(s)
        self.assertEqual(expected, actual)

    def test_removed_newline(self):
        s = "hello world\n"
        expected = "hello world"
        actual = extract_helpers.remove_newlines(s)
        self.assertEqual(expected, actual)

    def test_separate_punctuation(self):
        # only care about: [.?!]
        s = "hello world?? how are you. i am good!!!"
        expected = "hello world ?? how are you . i am good !!!"
        actual = extract_helpers.handle_punctuation(s)
        self.assertEqual(expected, actual)

    def test_removed_unwanted_punctuation(self):
        s = "hello: world, 'i am good', but are you good"
        expected = "hello world i am good but are you good"
        actual = extract_helpers.handle_punctuation(s)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
