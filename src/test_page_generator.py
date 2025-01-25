import unittest

from page_generator import extract_title


class TestPageGenerator(unittest.TestCase):
    def test_extract_title_simple_title(self):
        markdown = "# This is a title"
        expected = "This is a title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_extract_title_documentWithMultipleLines(self):
        markdown = "# This is a title\nthis is the next line"
        expected = "This is a title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_extract_title_documentWithMultipleLinesNoTitle(self):
        markdown = "This is not a title\nthis is the next line"
        self.assertRaises(ValueError, extract_title, markdown)

    def test_extract_title_simple_titleWithWhitespace(self):
        markdown = "# This is a title  "
        expected = "This is a title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)