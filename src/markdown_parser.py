import re
from typing import Callable

from textnode import TextNode, TextType


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
        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        new_nodes.append(TextNode(split_text[1], text_type))
        if split_text[2] == "":
            continue
        new_nodes.extend(split_nodes_delimiter([TextNode(split_text[2], TextType.TEXT)], delimiter, text_type))
    return new_nodes


# def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
#     new_nodes: list[TextNode] = []
#     for node in old_nodes:
#         text = node.text
#         matches = extract_markdown_images(text)
#         if len(matches) == 0:
#             new_nodes.append(node)
#             continue
#         match = matches[0]
#         split_text = text.split(f"![{match[0]}]({match[1]})", maxsplit=1)
#         new_nodes.append(TextNode(split_text[0], TextType.TEXT))
#         new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
#         if split_text[1] != "":
#             other_text = TextNode(split_text[1], TextType.TEXT)
#             new_nodes.extend(split_nodes_image([other_text]))
#     return new_nodes

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
