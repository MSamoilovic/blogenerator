import unittest

from nodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode("a", "click me", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "click me", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode("p", "hello", props={"class": "intro"})
        self.assertIn("HTMLNode", repr(node))
        self.assertIn("'p'", repr(node))
        self.assertIn("'hello'", repr(node))


if __name__ == "__main__":
    unittest.main()
