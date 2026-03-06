from nodes.textnode import TextNode, TextType
from markdown.extractor import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: unclosed delimiter '{delimiter}' in: {node.text!r}")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image_text, image_link in images:
            sections = original_text.split(f"![{image_text}]({image_link})", 1)

            if len(sections) != 2:
                continue

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_link))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link_text, link_url in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                continue
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

