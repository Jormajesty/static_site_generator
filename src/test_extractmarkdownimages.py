import unittest
from extract_markdown_images import extract_markdown_images

class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "Here is an image: ![alt text](https://example.com/image.png)"
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = (
            "Image 1: ![first image](https://example.com/first.png)\n"
            "Image 2: ![second image](https://example.com/second.jpg)\n"
            "Image 3: ![third image](https://example.com/third.gif)"
        )
        expected = [
            ("first image", "https://example.com/first.png"),
            ("second image", "https://example.com/second.jpg"),
            ("third image", "https://example.com/third.gif"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This text contains no markdown images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image(self):
        text = "This is a malformed image: ![alt text(https://example.com/image.png)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_alt_text_with_special_characters(self):
        text = "Image: ![alt text with (special) characters](https://example.com/image.png)"
        expected = [("alt text with (special) characters", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_whitespace(self):
        text = "Image: ![  alt text  ](  https://example.com/image.png  )"
        expected = [("  alt text  ", "  https://example.com/image.png  ")]
        self.assertEqual(extract_markdown_images(text), expected)

if __name__ == "__main__":
    unittest.main()