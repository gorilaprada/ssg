from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import extract_title, markdown_to_html_node
import os
import sys
import shutil

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_path = "static"
    content_path = "content"
    template_path = "template.html"
    target_path = "docs"
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    static_to_public(static_path, target_path)
    generate_pages_recursive(content_path, template_path, target_path, basepath)
    return

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    list_of_content_paths = os.listdir(dir_path_content)
    for content_path in list_of_content_paths:
        new_dir_path = os.path.join(dir_path_content, content_path)
        new_dest_path = os.path.join(dest_dir_path, content_path)
        if os.path.isfile(new_dir_path):
            new_dest_path = os.path.splitext(new_dest_path)[0] + ".html"
            generate_page(new_dir_path, template_path, new_dest_path, basepath)
        else:
            generate_pages_recursive(new_dir_path, template_path, new_dest_path, basepath)
    return

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} from {template_path}")
    # Storing md and template file as str
    with open(from_path, "r") as md_file:
        md = md_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    # Get html to inject in template
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    # Create HTML to inject from template
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", str(html))
    full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    # Write the new HTML page at destination path
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(full_html)
    return

def static_to_public(src: str, target: str) -> None:
    if not os.path.exists(target):
        os.mkdir(target)
    list_of_dir = os.listdir(src)
    for dir in list_of_dir:
        new_src = os.path.join(src, dir)
        new_target = os.path.join(target, dir)
        if os.path.isfile(new_src):
            shutil.copy(new_src, new_target)
            print(f"{new_src} copied to {new_target}")
        else:
            static_to_public(new_src, new_target)
    return




main()
