import os

from markdown.converter import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, entry)
        dst = os.path.join(dest_dir_path, entry)
        if os.path.isfile(src) and entry.endswith(".md"):
            generate_page(src, template_path, dst.replace(".md", ".html"), basepath)
        elif os.path.isdir(src):
            generate_pages_recursive(src, template_path, dst, basepath)

