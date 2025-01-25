import re
from enum import Enum, auto
from functools import reduce
from typing import Callable

from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED = auto()
    ORDERED = auto()


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter, maxsplit=2)
        if len(split_text) == 1:
            new_nodes.append(node)
            continue
        if len(split_text) == 2:
            raise ValueError(f"No closing delimiter '{delimiter}' found in text '{node.text}'")
        if split_text[0]:   # only add a text node if the first part is not empty. Can happen if string starts with delimiter.
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        new_nodes.append(TextNode(split_text[1], text_type))
        if split_text[2] == "":
            continue
        new_nodes.extend(split_nodes_delimiter([TextNode(split_text[2], TextType.TEXT)], delimiter, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(old_nodes, extract_markdown_images,
                       lambda x: f"![{x[0]}]({x[1]})",
                       TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(old_nodes, extract_markdown_links,
                       lambda x: f"[{x[0]}]({x[1]})",
                       TextType.LINK)


def split_nodes(old_nodes: list[TextNode],
                           match_func: Callable[[str], list[tuple[str, str]]],
                           str_func: Callable[[tuple], str],
                           text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        text = node.text
        matches = match_func(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        match = matches[0]
        split_text = text.split(str_func(match), maxsplit=1)
        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        new_nodes.append(TextNode(match[0], text_type, match[1]))
        if split_text[1] != "":
            other_text = TextNode(split_text[1], TextType.TEXT)
            new_nodes.extend(split_nodes([other_text], match_func, str_func, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)]\((.+?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)]\((.+?)\)", text)
    return matches


def extract_list_item(text_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for text_node in text_nodes:
        matches = re.findall(r"^((\*|\d+\.) )(.*)", text_node.text)
        if len(matches) == 0:
            new_nodes.append(text_node)
            continue
        new_nodes.append(TextNode(matches[0][-1].strip(), TextType.TEXT))
    return new_nodes


def line_to_textnodes(text: str) -> list[TextNode]:
    start_nodes = [TextNode(text, TextType.TEXT)]
    italic_extractor = lambda nodes: split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    bold_extractor = lambda nodes: split_nodes_delimiter(nodes, "**", TextType.BOLD)
    code_extractor = lambda nodes: split_nodes_delimiter(nodes, "`", TextType.CODE)
    list_nodes = extract_list_item(start_nodes)
    bold_nodes = bold_extractor(list_nodes)
    italic_nodes = italic_extractor(bold_nodes)
    code_nodes = code_extractor(italic_nodes)
    image_nodes = split_nodes_image(code_nodes)
    return split_nodes_link(image_nodes)


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    stripped_blocks = list()
    for block in raw_blocks:
        block = block.strip()
        if "\n" in block:
            block = "\n".join(list(map(lambda line: line.strip(), block.split("\n"))))
        stripped_blocks.append(block)
    return stripped_blocks


def all_lines_start_with(lines: list[str], start: str) -> bool:
    for line in lines:
        if not re.match(start, line):
            return False
    return True


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if re.match("#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all_lines_start_with(lines, "> "):
        return BlockType.QUOTE
    if all_lines_start_with(lines, r"\* "):
        return BlockType.UNORDERED
    if all_lines_start_with(lines, r"\d+\. "):
        return BlockType.ORDERED
    return BlockType.PARAGRAPH


# def text_to_leaf_nodes(text: str, tag: str = None) -> list[LeafNode]:
#     lines = text.split("\n")
#     list_text_nodes = list(map(line_to_textnodes, lines))
#     text_nodes = reduce(lambda x, y: x + y, list_text_nodes)
#     html_nodes = list(map(text_node_to_html_node, text_nodes))
#     if tag:
#         for node in html_nodes:
#             node.tag = tag
#     return html_nodes

def text_to_leaf_nodes(text: str, tag: str = None) -> list[LeafNode]:
    lines = text.split("\n")
    list_text_nodes = list(map(line_to_textnodes, lines))
    html_nodes = list()
    for text_node_list in list_text_nodes:
        line_html_nodes = list(map(text_node_to_html_node, text_node_list))
        if tag:
            html_nodes.append(ParentNode(tag, line_html_nodes))
        else:
            html_nodes.extend(line_html_nodes)
    if tag:
        for node in html_nodes:
            node.tag = tag
    return html_nodes


def code_block_to_html_node(block: str) -> HTMLNode:
    lines = block.replace("```", "").split("\n")
    stripped_lines = list(map(lambda line: line.strip(), lines))
    lines = filter(lambda line: line != "", stripped_lines)
    leaf_nodes = [LeafNode(None, line) for line in lines]
    return ParentNode("pre", [ParentNode("code", leaf_nodes)])


def quote_block_to_html_node(block: str) -> HTMLNode:
    lines = block.replace("> ", "").split("\n")
    stripped_lines = list(map(lambda line: line.strip(), lines))
    leaf_nodes = [LeafNode(None, line) for line in stripped_lines]
    return ParentNode("blockquote", leaf_nodes)


def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    match block_type:
        case BlockType.HEADING:
            heading_type, heading_value = block.split(" ", maxsplit=1)
            h_num = len(heading_type)
            return LeafNode(f"h{h_num}", heading_value)
        case BlockType.PARAGRAPH:
            leaf_nodes = text_to_leaf_nodes(block)
            return ParentNode("p", leaf_nodes)
        case BlockType.UNORDERED:
            leaf_nodes = text_to_leaf_nodes(block, "li")
            return ParentNode("ul", leaf_nodes)
        case BlockType.ORDERED:
            leaf_nodes = text_to_leaf_nodes(block, "li")
            return ParentNode("ol", leaf_nodes)
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = list()
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes.append(block_to_html_node(block, block_type))
    return ParentNode("div", child_nodes)


