from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, node_2):
        return (
            self.text == node_2.text
            and self.text_type == node_2.text_type
            and self.url == node_2.url
        )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    