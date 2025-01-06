from split_functions import split_nodes_delimiter, split_nodes_link
from textnode import TextNode, TextType


print("hello world!")

def main():
    # node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    # markdown_node = TextNode(
    #         "This is text with a **bolded word** and **another**", TextType.TEXT
    #     )
    # new_nodes = split_nodes_delimiter([markdown_node], "**", TextType.CODE)
    node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
    new_nodes = split_nodes_link([node])

main()