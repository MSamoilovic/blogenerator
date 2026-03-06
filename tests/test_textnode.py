import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_link(self):
        node = TextNode("This is a text link", TextType.LINK, "https://boot.dev.com")
        node2 = TextNode("This is a text link", TextType.LINK, "https://boot.dev.com")
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev.com")
        self.assertNotEqual(node, node2)

    def test_textnoneq(self):
        node = TextNode("TextA", TextType.TEXT)
        node2 = TextNode("TextB", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_linkexists(self):
         node = TextNode("Text A", TextType.LINK, "https://boot.dev.com")
         self.assertNotEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()