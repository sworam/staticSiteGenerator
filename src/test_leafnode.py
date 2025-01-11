import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_tagAndValue(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = '<p>This is a paragraph of text.</p>'
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_noTag(self):
        node = LeafNode(None, "This is a paragraph of text.")
        expected = 'This is a paragraph of text.'
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_oneProp(self):
        node = LeafNode("b", "This is a paragraph of text.", {"href": "https://www.google.com"})
        expected = '<b href="https://www.google.com">This is a paragraph of text.</b>'
        actual = node.to_html()
        self.assertEqual(actual, expected)

    def test_to_html_twoProps(self):
        node = LeafNode("p", "This is a paragraph of text.", {"href": "https://www.google.com", "target": "_blank"})
        expected = '<p href="https://www.google.com" target="_blank">This is a paragraph of text.</p>'
        actual = node.to_html()
        self.assertEqual(actual, expected)