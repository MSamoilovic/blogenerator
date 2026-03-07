import unittest

from nodes.textnode import TextNode, TextType
from markdown.delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_middle(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_code_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ])

    def test_code_at_end(self):
        node = TextNode("ends with `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_multiple_code_spans(self):
        node = TextNode("a `b` and `c` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("c", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_bold_middle(self):
        node = TextNode("Hello **world** today", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" today", TextType.TEXT),
        ])

    def test_bold_at_start(self):
        node = TextNode("**Bold** start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Bold", TextType.BOLD),
            TextNode(" start", TextType.TEXT),
        ])

    def test_bold_at_end(self):
        node = TextNode("end is **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("end is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_italic_middle(self):
        node = TextNode("say _hello_ there", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("say ", TextType.TEXT),
            TextNode("hello", TextType.ITALIC),
            TextNode(" there", TextType.TEXT),
        ])

    def test_italic_at_start(self):
        node = TextNode("_italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_no_delimiter_passes_through(self):
        node = TextNode("plain text no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_code_node_passes_through(self):
        node = TextNode("some `code`", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_mixed_list(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("split `this` up", TextType.TEXT),
            TextNode("no delimiters here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("already bold", TextType.BOLD),
            TextNode("split ", TextType.TEXT),
            TextNode("this", TextType.CODE),
            TextNode(" up", TextType.TEXT),
            TextNode("no delimiters here", TextType.TEXT),
        ])

    def test_chained_bold_then_italic(self):
        nodes = [TextNode("**bold** and _italic_ text", TextType.TEXT)]
        after_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_chained_code_then_bold(self):
        nodes = [TextNode("use `x` and **y** together", TextType.TEXT)]
        after_code = split_nodes_delimiter(nodes, "`", TextType.CODE)
        result = split_nodes_delimiter(after_code, "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("use ", TextType.TEXT),
            TextNode("x", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("y", TextType.BOLD),
            TextNode(" together", TextType.TEXT),
        ])

    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("missing `closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unclosed_bold_raises(self):
        node = TextNode("**no closing", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("text ![alt](https://img.com/a.png) end", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("text ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
            TextNode(" end", TextType.TEXT),
        ])

    def test_image_at_start(self):
        node = TextNode("![alt](https://img.com/a.png) after", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode("before ![alt](https://img.com/a.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
        ])

    def test_multiple_images(self):
        node = TextNode("![a](https://a.com/1.png) and ![b](https://b.com/2.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("a", TextType.IMAGE, "https://a.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "https://b.com/2.png"),
        ])

    def test_no_images_passes_through(self):
        node = TextNode("plain text no images", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_empty_list(self):
        self.assertEqual(split_nodes_image([]), [])


class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode("text [boot dev](https://www.boot.dev) end", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("text ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" end", TextType.TEXT),
        ])

    def test_link_at_start(self):
        node = TextNode("[click](https://example.com) after", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode("before [click](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("before ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://example.com"),
        ])

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ])

    def test_no_links_passes_through(self):
        node = TextNode("plain text no links", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_does_not_match_images(self):
        node = TextNode("![img](https://img.com/a.png)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])


class TestTextToTextnodes(unittest.TestCase):

    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_plain_text(self):
        result = text_to_textnodes("just plain text")
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_only_bold(self):
        result = text_to_textnodes("**bold**")
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_only_image(self):
        result = text_to_textnodes("![alt](https://example.com/img.png)")
        self.assertEqual(result, [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")])

    def test_only_link(self):
        result = text_to_textnodes("[click](https://example.com)")
        self.assertEqual(result, [TextNode("click", TextType.LINK, "https://example.com")])

    def test_bold_and_italic(self):
        result = text_to_textnodes("**bold** and _italic_")
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])


class TestMarkdownToBlocks(unittest.TestCase):

    def test_three_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ])

    def test_strips_whitespace(self):
        result = markdown_to_blocks("  # Heading  \n\n  paragraph  ")
        self.assertEqual(result, ["# Heading", "paragraph"])

    def test_removes_empty_blocks(self):
        result = markdown_to_blocks("first\n\n\n\nsecond")
        self.assertEqual(result, ["first", "second"])

    def test_single_block(self):
        result = markdown_to_blocks("just one block")
        self.assertEqual(result, ["just one block"])

    def test_empty_string(self):
        result = markdown_to_blocks("")
        self.assertEqual(result, [])

    def test_only_whitespace(self):
        result = markdown_to_blocks("   \n\n   \n\n   ")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
