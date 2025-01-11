import unittest

from htmlnode import ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_noChildren(self):
        node = ParentNode("p", list())
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_oneChildNoProps(self):
        node = ParentNode("p", [LeafNode(None, "First Child")])
        expected = "<p>First Child</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_oneChildTwoProps(self):
        node = ParentNode("p", [LeafNode(None, "First Child")],
                          {"href": "https://www.google.com", "target": "_blank"})
        expected = '<p href="https://www.google.com" target="_blank">First Child</p>'
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_twoChildrenTwoProps(self):
        node = ParentNode("p", [
            LeafNode(None, "First Child"),
            LeafNode("b", "Second Child", {"href": "boot.dev"}),],
                          {"href": "https://www.google.com", "target": "_blank"})
        expected = '<p href="https://www.google.com" target="_blank">First Child<b href="boot.dev">Second Child</b></p>'
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_nestedChildrenTwoProps(self):
        node = ParentNode("div", [ParentNode("p", [
            LeafNode(None, "First Child"),
            LeafNode("b", "Second Child", {"href": "boot.dev"})])],
                          {"href": "https://www.google.com", "target": "_blank"})
        expected = '<div href="https://www.google.com" target="_blank"><p>First Child<b href="boot.dev">Second Child</b></p></div>'
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_twoNestedChildrenTwoProps(self):
        node = ParentNode("div", [
                                    ParentNode("p", [
                                    LeafNode(None, "First Child"),
                                    LeafNode("b", "Second Child", {"href": "boot.dev"})]),
                                    ParentNode("p", [LeafNode("i", "Third Child"),]),
                                    LeafNode(None, "Fourth Child"),],
                          {"href": "https://www.google.com", "target": "_blank"})
        expected = '<div href="https://www.google.com" target="_blank"><p>First Child<b href="boot.dev">Second Child</b></p><p><i>Third Child</i></p>Fourth Child</div>'
        actual = node.to_html()
        self.assertEqual(expected, actual)