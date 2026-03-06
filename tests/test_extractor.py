import unittest

from markdown.extractor import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "![alt text](https://example.com/image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://example.com/image.png")])

    def test_multiple_images(self):
        text = "![first](https://a.com/1.png) and ![second](https://b.com/2.jpg)"
        self.assertEqual(extract_markdown_images(text), [
            ("first", "https://a.com/1.png"),
            ("second", "https://b.com/2.jpg"),
        ])

    def test_empty_alt_text(self):
        text = "![](https://example.com/image.png)"
        self.assertEqual(extract_markdown_images(text), [("", "https://example.com/image.png")])

    def test_no_images(self):
        text = "just plain text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_does_not_match_links(self):
        text = "[not an image](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_mixed_with_text(self):
        text = "Before ![img](https://example.com/img.png) after"
        self.assertEqual(extract_markdown_images(text), [("img", "https://example.com/img.png")])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_single_link(self):
        text = "[click here](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("click here", "https://example.com")])

    def test_multiple_links(self):
        text = "[first](https://a.com) and [second](https://b.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("first", "https://a.com"),
            ("second", "https://b.com"),
        ])

    def test_empty_link_text(self):
        text = "[](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("", "https://example.com")])

    def test_no_links(self):
        text = "just plain text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_does_not_match_images(self):
        text = "![image](https://example.com/img.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_mixed_with_image(self):
        text = "![img](https://example.com/img.png) and [link](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://example.com")])

    def test_link_mixed_with_text(self):
        text = "Click [here](https://example.com) to visit"
        self.assertEqual(extract_markdown_links(text), [("here", "https://example.com")])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_multiple_links_and_images(self):
        text = "![img](https://img.com/a.png) check [this](https://this.com) and [that](https://that.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("this", "https://this.com"),
            ("that", "https://that.com"),
        ])


if __name__ == "__main__":
    unittest.main()
