import os
from pathlib import Path
from models.htmlnode import HTMLNode
from helpers.block_conversion_helpers import markdown_to_htmlnode

def extract_header(md: str) -> str:
    lines = md.split('\n')
    for line in lines:
        if line == '':
            continue
        if line[0] == '#':
            return line[2:].strip()
    raise Exception("No heading found in md file")

def generate_page(src_path: str, template_path: str, dest_path: str):
    print(f"generating page from {src_path} to {dest_path} using {template_path}")
    try:
        with open(src_path) as src:
            src_content = src.read()
    except:
            raise Exception("failed to read {src_path}")
    try:
        with open(template_path) as template:
            template_content = template.read()
    except:
        raise Exception("failed to read {template_path}")

    src_in_html = markdown_to_htmlnode(src_content).to_html()
    title = extract_header(src_content)
    new_template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", src_in_html)


    dest_file = Path(dest_path)
    dest_file.parent.mkdir(exist_ok=True, parents=True)
    with open(dest_file, 'w') as file:
        file.write(new_template_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    try:
        content_dir_contents = os.listdir(dir_path_content)
        for file_item in content_dir_contents:
            content_file_item_path = os.path.join(dir_path_content, file_item)
            file_dest_dir_path = os.path.join(dest_dir_path, file_item)
            if os.path.isfile(content_file_item_path):
                file_dest_dir_path = file_dest_dir_path.replace('.md', '.html')
                generate_page(content_file_item_path, template_path, file_dest_dir_path)
            else:
                generate_pages_recursive(content_file_item_path, template_path, file_dest_dir_path)
    except:
        raise Exception("failed to generate pages, please check files in content/")