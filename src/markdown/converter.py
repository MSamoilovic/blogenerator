import re

from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode
from markdown.delimiter import text_to_textnodes, markdown_to_blocks
from markdown.blocks import BlockType, block_to_block_type
from markdown.inline import text_node_to_html_node


def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = len(re.match(r"^(#{1,6}) ", block).group(1))
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    content = block[4:-3]  # strip opening "```\n" and closing "```"
    code_node = text_node_to_html_node(TextNode(content, TextType.CODE))
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = [line.lstrip(">").lstrip(" ") for line in lines]
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    items = block.split("\n")
    li_nodes = [ParentNode("li", text_to_children(item[2:])) for item in items]
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    li_nodes = [ParentNode("li", text_to_children(item.split(". ", 1)[1])) for item in items]
    return ParentNode("ol", li_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children)
