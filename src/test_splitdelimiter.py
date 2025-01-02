import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):

    def test_valid_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node],"`", TextType.CODE)
        self.assertEqual(result, [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)] )

    # def test_no_backticks(self):
    #     text = "This is text with no code block word"
    #     result = split_nodes_delimiter(text)
    #     self.assertIsNone(result)

    # def test_empty_string(self):
    #     text = ""
    #     result = split_nodes_delimiter(text)
    #     self.assertIsNone(result)

    # def test_multiple_code_blocks(self):
    #     text = "This has `first` and `second` blocks"
    #     result = split_nodes_delimiter(text)
    #     self.assertEqual(result, (10, 15))  # Captures only the first block

    # def test_nested_backticks(self):
    #     text = "Nested `code `block` example"
    #     result = split_nodes_delimiter(text)
    #     self.assertEqual(result, (8, 22))  # Captures the first closing backtick

    # def test_code_block_at_start(self):
    #     text = "`start here` and continue"
    #     result = split_nodes_delimiter(text)
    #     self.assertEqual(result, (1, 11))

    # def test_code_block_at_end(self):
    #     text = "Continue until `the end`"
    #     result = split_nodes_delimiter(text)
    #     self.assertEqual(result, (15, 22))

if __name__ == "__main__":
    unittest.main()