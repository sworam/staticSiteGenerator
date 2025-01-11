import unittest

from htmlnode import HTMLNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


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

    def test_eq_no_values(self):
        first_node = HTMLNode()
        second_node = HTMLNode()
        self.assertEqual(first_node, second_node)

    def test_eq_tag(self):
        first_node = HTMLNode("a")
        second_node = HTMLNode("a")
        self.assertEqual(first_node, second_node)

    def test_eq_value(self):
        first_node = HTMLNode(None, "value")
        second_node = HTMLNode(None, "value")
        self.assertEqual(first_node, second_node)

    def test_eq_children(self):
        first_node = HTMLNode(children=[HTMLNode("a"), HTMLNode("b")])
        second_node = HTMLNode(children=[HTMLNode("a"), HTMLNode("b")])
        self.assertEqual(first_node, second_node)

    def test_eq_props(self):
        first_node = HTMLNode(props={"href": "https://www.google.com"})
        second_node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(first_node, second_node)

    def test_eq_differentTag_False(self):
        first_node = HTMLNode("a")
        second_node = HTMLNode("b")
        self.assertNotEqual(first_node, second_node)

    def test_eq_differentValue_False(self):
        first_node = HTMLNode(None, "value")
        second_node = HTMLNode(None, "different value")
        self.assertNotEqual(first_node, second_node)

    def test_eq_differentChildren_False(self):
        first_node = HTMLNode(children=[HTMLNode("a")])
        second_node = HTMLNode(children=[HTMLNode("b")])
        self.assertNotEqual(first_node, second_node)

    def test_eq_differentProps_False(self):
        first_node = HTMLNode(props={"href": "https://www.google.com"})
        second_node = HTMLNode(props={"href": "https://www.boot.dev"})
        self.assertNotEqual(first_node, second_node)

    def test_eq_multipleValues_True(self):
        first_node = HTMLNode("a", "value",
                              children=[HTMLNode("b"), HTMLNode("c")],
                              props={"href": "https://www.google.com"})
        second_node = HTMLNode("a", "value",
                              children=[HTMLNode("b"), HTMLNode("c")],
                              props={"href": "https://www.google.com"})
        self.assertEqual(first_node, second_node)

    def test_eq_multipleValues_False(self):
        first_node = HTMLNode("a", "value",
                              children=[HTMLNode("b"), HTMLNode("c")],
                              props={"href": "https://www.google.com"})
        second_node = HTMLNode("a", "value",
                              children=[HTMLNode("b"), HTMLNode("d")],
                              props={"href": "https://www.google.com"})
        self.assertNotEqual(first_node, second_node)



class TestNodeToHTML(unittest.TestCase):
    def test_text_node_to_html_TEXTType(self):
        text_node = TextNode("TextNode", TextType.TEXT)
        html_node = LeafNode(None, "TextNode")
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)

    def test_text_node_to_html_BOLDType(self):
        text_node = TextNode("BoldType", TextType.BOLD)
        html_node = LeafNode("b", "BoldType")
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)

    def test_text_node_to_html_ITALICType(self):
        text_node = TextNode("ItalicType", TextType.ITALIC)
        html_node = LeafNode("i", "ItalicType")
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)

    def test_text_node_to_html_CODEType(self):
        text_node = TextNode("CodeType", TextType.CODE)
        html_node = LeafNode("code", "CodeType")
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)

    def test_text_node_to_html_LINKType(self):
        text_node = TextNode("LinkType", TextType.LINK, url="https://www.google.com")
        html_node = LeafNode("a", "LinkType", props={"href": "https://www.google.com"})
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)

    def test_text_node_to_html_IMAGEType(self):
        text_node = TextNode("ImageType", TextType.IMAGE,
                             url="https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = LeafNode("img", "",
                             props={"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp",
                                    "alt": "ImageType"})
        actual = text_node_to_html_node(text_node)
        self.assertEqual(actual, html_node)