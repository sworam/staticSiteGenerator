from enum import Enum, auto


class TextType(Enum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True
    
    def __repr__(self):
        text, text_type, url = self.text, self.text_type, self.url
        return f"TextNode({text=}, {text_type=}, {url=})"
