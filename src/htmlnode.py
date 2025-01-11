from typing import Self


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


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Value required in LeafNode.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
