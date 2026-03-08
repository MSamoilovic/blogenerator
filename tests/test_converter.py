import unittest

from markdown.converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_h1(self):
        md = "# Hello World"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Hello World</h1></div>")

    def test_heading_h3_with_inline(self):
        md = "### A **bold** heading"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h3>A <b>bold</b> heading</h3></div>")

    def test_blockquote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote</blockquote></div>")

    def test_blockquote_multiline(self):
        md = "> line one\n> line two"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>line one line two</blockquote></div>")

    def test_unordered_list(self):
        md = "- first\n- second\n- third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = "- **bold** item\n- _italic_ item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Title

A paragraph here.

- item one
- item two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>A paragraph here.</p><ul><li>item one</li><li>item two</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
