import os
import shutil
from functions_2 import *

def copy_items(directory, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    
    def helper(directory, target, path='./'):
        dir_path = path + directory + "/"
        target_path = dir_path.replace("static", "public")
        
        for item in os.listdir(dir_path):
            if os.path.isfile(dir_path + item):
                shutil.copy(dir_path + item, target_path)
            else:
                os.makedirs((target_path + item), exist_ok=True)
                helper(item, target, dir_path)
    
    helper(directory, target)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating fage from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as file:
        markdown = file.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    with open(template_path, "r") as file:
        template = file.read()
        filled = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    with open(dest_path, "w") as file:
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
        file.write(filled)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path = dir_path_content + "/"
    target_path = dir_path.replace("content", "public")
    
    for item in os.listdir(dir_path):
        if item == "index.md":
            generate_page(dir_path + item, template_path, target_path + item.replace("md", "html"))
        elif os.path.isdir(dir_path + item):
            os.makedirs((target_path + item), exist_ok=True)
            generate_pages_recursive(dir_path + item, template_path, target_path)

copy_items("static","public")
generate_pages_recursive("content", "template.html", "public")