import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path
"""
    This function extracts the header
"""
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No header found")

"""
"""
def generate_page(from_path, template_path, dest_path):
    var_markdown = None
    var_template = None
    print(f"Generating page from {from_path} to {dest_path}, {template_path}")
    #read the markdown file at from_path and store in a variable
    with open(from_path, 'r') as f:
        var_markdown = f.read()
    #read the template file at template_path and store in a variable
    with open(template_path, 'r') as f:
        var_template = f.read()
    
    node = markdown_to_html_node(var_markdown)
    html_content = node.to_html()

    title = extract_title(var_markdown)

    final_html = var_template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    #write html content into dest_path
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as f:
        f.write(final_html)

    
"""
    generate html pages using recursion
"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # iterate through the source directory (./content)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
            
