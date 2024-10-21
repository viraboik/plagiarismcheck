import unittest

from utils import split_text_by_words


class TestSplitTextByWords(unittest.TestCase):
    def test_split_text_simple(self):
        text = "aaa bbb ccc, ddd. "
        expected_result = [
            ('aaa', 0, 3),
            ('bbb', 4, 7),
            ('ccc', 8, 11),
            (',', 11, 12),
            ('ddd', 13, 16),
            ('.', 16, 17)
        ]
        result = split_text_by_words(text)
        self.assertEqual(result, expected_result)

    def test_split_text_with_multiple_spaces(self):
        text = "word1   word2"
        expected_result = [
            ('word1', 0, 5),
            ('word2', 8, 13)
        ]
        result = split_text_by_words(text)
        self.assertEqual(result, expected_result)

    def test_split_text_empty(self):
        text = ""
        expected_result = []
        result = split_text_by_words(text)
        self.assertEqual(result, expected_result)

    def test_split_text_special_characters(self):
        text = "@test!"
        expected_result = [
            ('@', 0, 1),
            ('test', 1, 5),
            ('!', 5, 6)
        ]
        result = split_text_by_words(text)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
