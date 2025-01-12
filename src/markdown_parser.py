import re
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([\w ]*)]\(([\w/:.]+)\)", text)
    return matches
