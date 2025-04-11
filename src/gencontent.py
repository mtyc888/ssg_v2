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
def generate_page(from_path, template_path, output_path, basepath="/"):
    var_markdown = None
    var_template = None
    print(f"Generating page from {from_path} to {output_path} with basepath {basepath}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        var_markdown = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        var_template = f.read()
    
    node = markdown_to_html_node(var_markdown)
    html_content = node.to_html()

    title = extract_title(var_markdown)

    final_html = var_template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace relative URLs with the basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Create directory if it doesn't exist
    dest_dir = os.path.dirname(output_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write to the output file (not the basepath)
    with open(output_path, "w") as f:
        f.write(final_html)

    
"""
    generate html pages using recursion
"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # iterate through the source directory (./content)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
            
