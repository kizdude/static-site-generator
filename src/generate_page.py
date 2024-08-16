from block_processing import markdown_to_blocks
from create_html import markdown_to_html_node

import os, pathlib

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block[:2] == "# ":
            return block[2:].strip()
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_contents = ""
    with open(from_path, "r") as markdown_file:
        markdown_contents = markdown_file.read()

    html_node = markdown_to_html_node(markdown_contents)
    html_string = html_node.to_html()

    title = extract_title(markdown_contents)

    template_contents = ""
    with open(template_path, "r") as template_file:
        template_contents = template_file.read()

    new_contents = template_contents.replace("{{ Title }}", title, 1)
    new_contents = new_contents.replace("{{ Content }}", html_string, 1)

    with open(dest_path, "w") as dest_file:
        dest_file.write(new_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # dir_path_content = "static/content/"
    # template_path = "template.html"
    # dest_dir_path = "public/"
    current_path_name = dir_path_content

    sub_paths = os.listdir(current_path_name)
    for sub_path in sub_paths:   
        if os.path.isfile(os.path.join(current_path_name, sub_path)):
            if sub_path == "index.md":
                dest_file = "index.html"
                generate_page(os.path.join(current_path_name, sub_path), template_path, os.path.join(dest_dir_path, dest_file))   
            else:
                continue
        else:
            generate_pages_recursive(os.path.join(current_path_name, sub_path), template_path, os.path.join(dest_dir_path, sub_path))

