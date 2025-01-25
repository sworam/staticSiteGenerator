import os

from markdown_parser import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split('\n')
    title_lines = list(filter(lambda line: line.startswith('# '), lines))
    if not title_lines:
        raise ValueError("No title found.")
    title = title_lines[0].strip("#").strip()
    return title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    out_text = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(dest_path, 'w') as f:
        f.write(out_text)
