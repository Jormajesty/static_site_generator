import unittest

from split_functions import block_to_block_type, markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINKS, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    # def test_text_to_textnodes(self):
    #     nodes = text_to_textnodes(
    #         "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    #     )
    #     self.assertListEqual(
    #         [
    #             TextNode("This is ", TextType.TEXT),
    #             TextNode("text", TextType.BOLD),
    #             TextNode(" with an ", TextType.TEXT),
    #             TextNode("italic", TextType.ITALIC),
    #             TextNode(" word and a ", TextType.TEXT),
    #             TextNode("code block", TextType.CODE),
    #             TextNode(" and an ", TextType.TEXT),
    #             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #             TextNode(" and a ", TextType.TEXT),
    #             TextNode("link", TextType.LINKS, "https://boot.dev"),
    #         ],
    #         nodes,
    #     )
    # def test_basic_markdown(self):
    #     markdown = """
    #     # This is a heading

    #     This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    #     * This is the first list item in a list block
    #     * This is a list item
    #     * This is another list item
    #     """
    #     expected = [
    #         "# This is a heading",
    #         "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
    #         "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    #     ]
    #     self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_markdown(self):
        markdown = """
        """
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_newlines(self):
        markdown = """

        """
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blocks(self):
        markdown = """
        Block 1

        Block 2

        Block 3
        """
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("## Heading text"), "heading")
        self.assertEqual(block_to_block_type("# Single level heading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), "code block")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote\n> Another line of quote"), "quote block")

    def test_unordered_list_block(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered list block")
        self.assertEqual(block_to_block_type("- Item A\n- Item B"), "unordered list block")

    def test_ordered_list_block(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), "ordered list block")
        self.assertEqual(block_to_block_type("1. Another first item\n2. Another second item\n3. Third item"), "ordered list block")

    def test_normal_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), "normal paragraph")
        self.assertEqual(block_to_block_type("Just some text."), "normal paragraph")

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_simple_markdown(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n* Item 1\n* Item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(str(html_node), "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>Item 1</li><li>Item 2</li></ul></div>")



if __name__ == "__main__":
    unittest.main()