import unittest

from markdown_parser import split_nodes_delimiter, TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_noSubNode(self):
        old_nodes = [TextNode("Text", TextType.TEXT)]
        expected_nodes = [TextNode("Text", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_oneSubNode(self):
        old_nodes = [TextNode("Text and **test**", TextType.TEXT)]
        expected_nodes = [TextNode("Text and ", TextType.TEXT),
                          TextNode("test", TextType.BOLD)]
        actual_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_twoSubNode(self):
        old_nodes = [TextNode("Text and *test* and *test2*", TextType.TEXT)]
        expected_nodes = [TextNode("Text and ", TextType.TEXT),
                          TextNode("test", TextType.ITALIC),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("test2", TextType.ITALIC)]
        actual_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_codeBlock(self):
        old_nodes = [TextNode("Text and `code`", TextType.TEXT)]
        expected_nodes = [TextNode("Text and ", TextType.TEXT),
                          TextNode("code", TextType.CODE)]
        actual_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_boldDelimiterItalicText(self):
        old_nodes = [TextNode("Text and **bold** and *italic*", TextType.TEXT)]
        expected_nodes = [TextNode("Text and ", TextType.TEXT),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" and *italic*", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_boldAndItalicDelimiterBoldAndItalicText(self):
        old_nodes = [TextNode("Text and **bold** and *italic*", TextType.TEXT)]
        expected_nodes = [TextNode("Text and ", TextType.TEXT),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("italic", TextType.ITALIC)]
        actual_nodes = split_nodes_delimiter(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
            "*", TextType.ITALIC)
        self.assertEqual(actual_nodes, expected_nodes)
