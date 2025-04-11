import os
import shutil
import sys
from gencontent import generate_page, generate_pages_recursive
def main():
    #delete everything in public directory
    clear_public("./docs")
    #copy all contents from static to public
    static_to_public("./static", "./docs")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    #generate a page
    generate_pages_recursive("./content","./template.html", "./docs")

def clear_public(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("error in clearing")

"""
    This function copies from source directory to destination directory
"""
def static_to_public(source_path, destination_path):
    try:
        # Ensure the destination directory exists
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        # List all files and directories in the current source_path
        files = os.listdir(source_path)
        for file in files:
            file_path = os.path.join(source_path, file)
            dest_file_path = os.path.join(destination_path, file)
            
            if os.path.isfile(file_path):
                # Copy file to the destination
                shutil.copy(file_path, dest_file_path)
            elif os.path.isdir(file_path):
                # Recursive call for the subdirectory
                static_to_public(file_path, dest_file_path)
        
        print(f"Content from {source_path} copied to {destination_path}")

    except OSError as e:
        print(f"Error occurred: {e}")
main()