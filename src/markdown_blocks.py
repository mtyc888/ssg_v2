from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from markdown_to_text import text_to_textnodes
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
"""
    This function takes a single block of markdown text as input and returns the
    BlockType representing the type of block it is.
"""
def block_to_block_type(markdown_block):
    lines = markdown_block.split('\n')
    if markdown_block.startswith(("#", "##", "###", "####", "#####", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return BlockType.CODE
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        index = 1
        for line in lines:
            if not line.startswith(f"{index}. "):
                return BlockType.PARAGRAPH
            index += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
"""
    This function takes a raw markdown string (full document) as input and returns
    a list of "block" strings.
"""
def markdown_to_blocks(markdown):
    # split the entire document into chunks
    markdown_blocks = markdown.split("\n\n")
    markdown_blocks_strip = []
    for block in markdown_blocks:
        block = block.strip()
        if block == "":
            continue
        markdown_blocks_strip.append(block)
    return markdown_blocks_strip

"""
    This function converts a full markdown document into a single parent HTMLNode
"""
def markdown_to_html_node(markdown):
    # split the markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    # parent node that holds all blocks
    
    list_of_children = []
    # loop over each block
    for block in markdown_blocks:
        #1. determine the type of block
        #2. based on the type of block, create a new HTMLNode with the proper data
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                paragraph_lines = block.split("\n")
                cleaned_lines = []

                for line in paragraph_lines:
                    stripped_line = line.strip()
                    if stripped_line:
                        cleaned_lines.append(stripped_line)

                if cleaned_lines:
                    paragraph_content = " ".join(cleaned_lines)
                else:
                    paragraph_content = ""

                paragraph_node = ParentNode("p", text_to_children(paragraph_content))
                list_of_children.append(paragraph_node)
                
            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                #remove the "#" characters (markdown for header)
                content = block[level:].lstrip()
                heading_node = ParentNode(f"h{level}", text_to_children(content))
                list_of_children.append(heading_node)

            case BlockType.CODE:
                code_content = block[4:-3]
                text_node = TextNode(code_content, TextType.TEXT)

                code_node_raw = text_node_to_html_node(text_node)
                """
                    has to be in this format <pre><code></code></pre>
                """
                code_node = ParentNode("code", [code_node_raw])
                final_code_node = ParentNode("pre", [code_node])

                list_of_children.append(final_code_node)
            
            case BlockType.QUOTE:
                lines = block.split("\n")
                quote_lines = []
                for line in lines:
                    line = line.lstrip(">").strip()
                    if line:
                        quote_lines.append(line)
                quote_content = " ".join(quote_lines)
                quote_node = ParentNode("blockquote", text_to_children(quote_content))
                list_of_children.append(quote_node)
            
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                
                ulist_nodes = []
                #remove the '- '
                for line in lines:
                    line = line.lstrip("- *").lstrip()
                    li_children = text_to_children(line)
                    li_node = ParentNode("li", li_children)
                    ulist_nodes.append(li_node)
                #create <ul> node with ulist_nodes as children <li>
                ulist_node = ParentNode("ul", ulist_nodes)
                list_of_children.append(ulist_node)
            
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                olist_nodes = []
                index = 1
                # remove the numbers
                for line in lines:
                    # finds the first occurence of ". " and removes it and everything before it 
                    if ". " in line:
                        line = line.split(". ", 1)[1]
                    ol_children = text_to_children(line)
                    ol_node = ParentNode("li", ol_children)
                    olist_nodes.append(ol_node)
                    index += 1
                olist_node = ParentNode("ol", olist_nodes)
                list_of_children.append(olist_node)

            case _:
                raise Exception("invalid block type")
        parent_node = ParentNode("div", list_of_children)
    return parent_node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

