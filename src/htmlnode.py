from typing import Self

from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[Self] = None, props: dict[str, str] = None):
        """

        :param tag: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        :param value: A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        :param children: A list of HTMLNode objects representing the children of this node
        :param props: A dictionary of key-value pairs representing the attributes of the HTML tag.
        For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        html_props = ""
        if not self.props:
            return html_props
        for prop, value in self.props.items():
            html_props += f' {prop}="{value}"'
        return html_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag=}, {self.value=}, children={len(self.children)}, props={self.props_to_html()})"

    def __eq__(self, other: Self) -> bool:
        if not self.tag == other.tag:
            return False
        if not self.value == other.value:
            return False
        if not self.children == other.children:
            return False
        if not self.props == other.props:
            return False
        return True


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Value required in LeafNode.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag required in ParentNode.")
        if not self.children or len(self.children) == 0:
            raise ValueError("Children required in ParentNode.")
        inner_text = "".join(list(map(lambda x: x.to_html(), self.children)))
        return f"<{self.tag}{self.props_to_html()}>{inner_text}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type {text_node.text_type}")
