from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


print("hello world!")

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    markdown_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([markdown_node], "`", TextType.CODE)
    print(node)
    print(new_nodes)
main()