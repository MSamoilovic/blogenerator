import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_props(self):
        node = ParentNode("a", [LeafNode(None, "click")], {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click</a>')

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [ParentNode("section", [ParentNode("p", [LeafNode("b", "deep")])])]
        )
        self.assertEqual(node.to_html(), "<div><section><p><b>deep</b></p></section></div>")

    def test_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_mixed_parent_and_leaf_children(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "item one")]),
                ParentNode("li", [LeafNode(None, "item two")]),
            ],
        )
        self.assertEqual(node.to_html(), "<ul><li><b>item one</b></li><li>item two</li></ul>")


if __name__ == "__main__":
    unittest.main()
