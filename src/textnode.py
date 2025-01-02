from enum import Enum 
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINKS = 'links'
    IMAGES = 'images'

class TextNode:
    def __init__(self,text, text_type,TextTypeurl=None):
        self.text = text
        self.text_type = text_type
        self.TextTypeurl = TextTypeurl

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text_type == other.text_type
                and self.text == other.text
                and self.TextTypeurl == other.TextTypeurl
            )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.TextTypeurl})"
def text_node_to_html_node(text_node):
    node = LeafNode(text_node.text)
    node.attributes['class'] = text_node.text_type.name
    if text_node.TextTypeurl:
        node.attributes['href'] = text_node.TextTypeurl
    return node