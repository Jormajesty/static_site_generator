import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        self.assertEqual(node, node2)
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.ITALIC, 'https://www.boot.dev')
        self.assertNotEqual(node, node2)
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        node2 = TextNode("This is not a text node", TextType.BOLD, 'https://www.boot.dev')
        self.assertNotEqual(node, node2)
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TEXT, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()