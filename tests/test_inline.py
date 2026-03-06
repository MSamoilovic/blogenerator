import unittest

from nodes.textnode import TextNode, TextType
from markdown.inline import text_node_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")

    def test_italic(self):
        node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/img.png", "alt": "alt text"})

    def test_renders_to_html(self):
        node = TextNode("Click me", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Click me</a>')

    def test_invalid_type_raises(self):
        node = TextNode("text", TextType.TEXT)
        node.text_type = "not_a_type"
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
