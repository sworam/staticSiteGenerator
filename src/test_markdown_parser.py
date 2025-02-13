import unittest

from markdown_parser import (split_nodes_delimiter, TextNode, TextType, extract_markdown_images, split_nodes_image,
                             split_nodes_link, extract_markdown_links, line_to_textnodes, markdown_to_blocks, BlockType,
                             block_to_block_type, markdown_to_html_node)
from htmlnode import ParentNode, LeafNode


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

    def test_split_nodes_delimiter_oneSubNodeBoldAtStart(self):
        old_nodes = [TextNode("**Bold** and normal", TextType.TEXT)]
        expected_nodes = [TextNode("Bold", TextType.BOLD),
                          TextNode(" and normal", TextType.TEXT)]
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_no_image(self):
        text = "This is text without an image"
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_broken_image(self):
        text = "This is text with ![broken](image"
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_no_alt(self):
        text = "This is text with image ![](withoutAlt)"
        expected = [("", "withoutAlt")]
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_no_url(self):
        text = "This is text without ![url]()"
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_one_image(self):
        text = r"This is text with ![one](https://image.png)"
        expected = [("one", "https://image.png")]
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_two_images(self):
        text = r"This is text with ![two](https://image.png) images ![with](https://other.image/image.png)"
        expected = [("two", "https://image.png"), ("with", "https://other.image/image.png")]
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_no_link(self):
        text = "This is text without an link"
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_broken_link(self):
        text = "This is text with [broken](link"
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_no_alt(self):
        text = "This is text with link [](withoutAlt)"
        expected = [("", "withoutAlt")]
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_no_url(self):
        text = "This is text without [url]()"
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_one_link(self):
        text = r"This is text with [one](https://boot.dev)"
        expected = [("one", "https://boot.dev")]
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_two_links(self):
        text = r"This is text with [two](https://boot.dev) links [with](https://other.link/boot.dev)"
        expected = [("two", "https://boot.dev"), ("with", "https://other.link/boot.dev")]
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_no_image(self):
        old_nodes = [TextNode("Text and *test* and *test2*", TextType.TEXT)]
        expected_nodes = [TextNode("Text and *test* and *test2*", TextType.TEXT)]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_oneImage(self):
        old_nodes = [TextNode("Text with ![image](https://image.png)", TextType.TEXT)]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, url="https://image.png")]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_brokenImage(self):
        old_nodes = [TextNode("text with broken image ![alt text](https://image.png", TextType.TEXT)]
        expected_nodes = [TextNode("text with broken image ![alt text](https://image.png", TextType.TEXT)]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_no_alt(self):
        old_nodes = [TextNode("text with no alt ![](https://image.png)", TextType.TEXT)]
        expected_nodes = [TextNode("text with no alt ", TextType.TEXT),
                          TextNode("", TextType.IMAGE, url="https://image.png")]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_imageSurroundedByText(self):
        old_nodes = [TextNode("Image is surrounded ![alt text](https://image.png) by text.", TextType.TEXT)]
        expected_nodes = [TextNode("Image is surrounded ", TextType.TEXT),
                          TextNode("alt text", TextType.IMAGE, url="https://image.png"),
                          TextNode(" by text.", TextType.TEXT)]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_twoNodesWithImage(self):
        old_nodes = [TextNode("Text with ![image](https://image.png)", TextType.TEXT),
                     TextNode("Text with another ![image2](https://image2.png)", TextType.TEXT)]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, url="https://image.png"),
                          TextNode("Text with another ", TextType.TEXT),
                          TextNode("image2", TextType.IMAGE, url="https://image2.png")]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_image_twoImages(self):
        old_nodes = [TextNode("Text with ![image](https://image.png) ![image2](https://image2.png)", TextType.TEXT),]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, url="https://image.png"),
                          TextNode(" ", TextType.TEXT),
                          TextNode("image2", TextType.IMAGE, url="https://image2.png")]
        actual = split_nodes_image(old_nodes)
        self.assertEqual(actual, expected_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_no_link(self):
        old_nodes = [TextNode("Text and *test* and *test2*", TextType.TEXT)]
        expected_nodes = [TextNode("Text and *test* and *test2*", TextType.TEXT)]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_oneLink(self):
        old_nodes = [TextNode("Text with [link](https://boot.dev)", TextType.TEXT)]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("link", TextType.LINK, url="https://boot.dev")]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_brokenLink(self):
        old_nodes = [TextNode("text with broken link [alt text](https://boot.dev", TextType.TEXT)]
        expected_nodes = [TextNode("text with broken link [alt text](https://boot.dev", TextType.TEXT)]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_no_alt(self):
        old_nodes = [TextNode("text with no alt [](https://boot.dev)", TextType.TEXT)]
        expected_nodes = [TextNode("text with no alt ", TextType.TEXT),
                          TextNode("", TextType.LINK, url="https://boot.dev")]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_AtChar(self):
        old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and "
                              "[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        expected_nodes = [TextNode("This is text with a link ", TextType.TEXT),
                          TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev")]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_linkSurroundedByText(self):
        old_nodes = [TextNode("link is surrounded [alt text](https://boot.dev) by text.", TextType.TEXT)]
        expected_nodes = [TextNode("link is surrounded ", TextType.TEXT),
                          TextNode("alt text", TextType.LINK, url="https://boot.dev"),
                          TextNode(" by text.", TextType.TEXT)]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_twoNodesWithLink(self):
        old_nodes = [TextNode("Text with [link](https://boot.dev)", TextType.TEXT),
                     TextNode("Text with another [link2](https://google.com)", TextType.TEXT)]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("link", TextType.LINK, url="https://boot.dev"),
                          TextNode("Text with another ", TextType.TEXT),
                          TextNode("link2", TextType.LINK, url="https://google.com")]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)

    def test_split_nodes_link_twoLinks(self):
        old_nodes = [TextNode("Text with [link](https://boot.dev) [link2](https://google.com)", TextType.TEXT),]
        expected_nodes = [TextNode("Text with ", TextType.TEXT),
                          TextNode("link", TextType.LINK, url="https://boot.dev"),
                          TextNode(" ", TextType.TEXT),
                          TextNode("link2", TextType.LINK, url="https://google.com")]
        actual = split_nodes_link(old_nodes)
        self.assertEqual(actual, expected_nodes)


class TestLineToTextnodes(unittest.TestCase):
    def test_line_to_text_nodes_differentTextTypes(self):
        text = ("This is **text** with an *italic* word and a `code block` "
                "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_plainText(self):
        text = "This is plain text."
        expected = [TextNode("This is plain text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_boldText(self):
        text = "Text with **bold** text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_italicText(self):
        text = "Text with *italic* text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_italicAndBoldText(self):
        text = "Text with *italic* and **bold** text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_codeText(self):
        text = "Text with `code` text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("code", TextType.CODE),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_imageText(self):
        text = "Text with ![image](https://image.png) text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, url="https://image.png"),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_linkText(self):
        text = "Text with [to bootdev](https://boot.dev) text."
        expected = [TextNode("Text with ", TextType.TEXT),
                    TextNode("to bootdev", TextType.LINK, url="https://boot.dev"),
                    TextNode(" text.", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_justLink(self):
        text = "[to bootdev](https://boot.dev)"
        expected = [TextNode("to bootdev", TextType.LINK, url="https://boot.dev")]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_line_to_text_nodes_listItem(self):
        text = "* this is an unordered list item"
        expected = [TextNode("this is an unordered list item", TextType.TEXT)]
        actual = line_to_textnodes(text)
        self.assertEqual(actual, expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_oneBlock(self):
        text = "# This is a heading"
        expected = ["# This is a heading"]
        actual = markdown_to_blocks(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_twoBlocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text."
        expected = ["# This is a heading", "This is a paragraph of text."]
        actual = markdown_to_blocks(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_threeBlocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text.\n\n* This is a list\n* another item\n* and another item"
        expected = ["# This is a heading", "This is a paragraph of text.", "* This is a list\n* another item\n* and another item"]
        actual = markdown_to_blocks(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_whitespace(self):
        text = "# This is a heading\n\n\nThis is a paragraph of text."
        expected = ["# This is a heading", "This is a paragraph of text."]
        actual = markdown_to_blocks(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_whitespaceInBlock(self):
        text = "# This is a heading\n\nThis is a paragraph of text.\n\n* This is a list\n* another item  \n* and another item"
        expected = ["# This is a heading", "This is a paragraph of text.", "* This is a list\n* another item\n* and another item"]
        actual = markdown_to_blocks(text)
        self.assertEqual(actual, expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "### This is a heading"
        expected = BlockType.HEADING
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        expected = BlockType.CODE
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_codeNotClosed_paragraph(self):
        block = "```\nThis is a code block"
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> in multiple lines"
        expected = BlockType.QUOTE
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_brokenQuote(self):
        block = "> This is a quote\n in multiple lines"
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_unorderedList(self):
        block = "* This is a unordered\n* list\n* in multiple lines"
        expected = BlockType.UNORDERED
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_brokenUnorderedList(self):
        block = "* This is a unordered\n1. list\n* in multiple lines"
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_orderedList(self):
        block = "1. This is a unordered\n3. list\n2. in multiple lines"
        expected = BlockType.ORDERED
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_orderedListHighOrder(self):
        block = "1. This is a unordered\n3. list\n20. in multiple lines"
        expected = BlockType.ORDERED
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_brokenOrderedList(self):
        block = "1. This is a unordered\n* list\n2. in multiple lines"
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)

    def test_block_to_block_type_normalParagraph(self):
        block = "This is a *normal* paragraph with **some** inline `code`."
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(actual, expected)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        text = "# Heading\n\nParagraph of **bold** text"
        expected = ParentNode("div", [
            LeafNode("h1", "Heading"),
            ParentNode("p", [
                LeafNode(None, "Paragraph of "),
                LeafNode("b", "bold"),
                LeafNode(None, " text"),
            ]),
        ])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_html_node_Lists(self):
        text = "* Unordered\n* List\n\n1. Ordered\n2. List"
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Unordered")]),
                ParentNode("li", [LeafNode(None, "List")])
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "Ordered")]),
                ParentNode("li", [LeafNode(None, "List")])
            ])
        ])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_html_node_ListWithSubNodes(self):
        text = "* Unordered\n* italic *List*"
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Unordered")]),
                ParentNode("li", [LeafNode(None, "italic "), LeafNode("i", "List")]),
            ])])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)

    def test_markdown_to_html_node_code(self):
        text = "```\nThis is code inside a code block\nThis is the second code line\n```"
        expected = ParentNode("div", [
            ParentNode("pre", [ParentNode("code", [
                LeafNode(None, "This is code inside a code block"),
                LeafNode(None, "This is the second code line")
            ])])
        ])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)


    def test_markdown_to_html_node_paragraphWithDifferentInlines(self):
        text = "This is a **bold** paragraph with different *italic* inline `code` blocks like ![images](https://image.png) and links [to obsidian](https://obsidian.md)."
        expected = ParentNode("div", [ParentNode("p", [
            LeafNode(None, "This is a "),
            LeafNode("b", "bold"),
            LeafNode(None, " paragraph with different "),
            LeafNode("i", "italic"),
            LeafNode(None, " inline "),
            LeafNode("code", "code"),
            LeafNode(None, " blocks like "),
            LeafNode("img", "", {"src": "https://image.png", "alt": "images"}),
            LeafNode(None, " and links "),
            LeafNode("a", "to obsidian", {"href": "https://obsidian.md"}),
            LeafNode(None, ".")
        ])])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)


    def test_markdown_to_html_node_blockquote(self):
        text = "> This is a block quote\n> in multiple lines."
        expected = ParentNode("div", [ParentNode("blockquote", [
            LeafNode(None, "This is a block quote"),
            LeafNode(None, "in multiple lines.")
        ])])
        actual = markdown_to_html_node(text)
        self.assertEqual(actual, expected)
