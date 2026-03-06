import unittest

from nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_anchor(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("a", "link", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">link</a>')

    def test_leaf_repr(self):
        node = LeafNode("p", "hello")
        self.assertIn("LeafNode", repr(node))


if __name__ == "__main__":
    unittest.main()
