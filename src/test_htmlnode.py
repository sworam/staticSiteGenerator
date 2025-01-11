import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_oneProp(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_props_to_html_twoProps(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_props_to_html_threeProps(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank", "class": "relative"})
        expected = ' href="https://www.google.com" target="_blank" class="relative"'
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_props_to_html_noProps(self):
        node = HTMLNode()
        expected = ""
        actual = node.props_to_html()
        self.assertEqual(actual, expected)
