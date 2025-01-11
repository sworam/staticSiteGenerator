import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_type_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.NORMAL, "URL")
        node2 = TextNode("This is a text node", TextType.NORMAL, "URL")
        self.assertEqual(node, node2)

    def test_non_eq_differentText(self):
        node = TextNode("This is not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_differentTextType(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_onlyOneUrl(self):
        node = TextNode("This is a text node", TextType.BOLD, "URL")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_differentUrl(self):
        node = TextNode("This is a text node", TextType.BOLD, "URL")
        node2 = TextNode("This is a text node", TextType.BOLD, "Other URL")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()