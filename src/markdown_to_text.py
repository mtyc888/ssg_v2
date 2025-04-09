from textnode import TextType, TextNode
import re
"""
    takes the old node, delimiter and text_type then return a list of
    new nodes that is split into different TextNodes.
    eg.

    This is text with a **bolded phrase** in the middle

    becomes:

    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),
    ]
"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # handle splitting the text based on delimiters
        text = old_node.text

        while delimiter in text:

            # find the first delimiter
            start_index = text.find(delimiter)

            # find the matching closing delimiter
            # we start searching from (start_index + len(delimiter)) to skip over the opening delimiter
            end_index = text.find(delimiter, start_index + len(delimiter))

            if end_index == -1:
                # there is no closing delimiter
                raise Exception(f"Missing closing delimiter for {delimiter}")
            
            # split text into parts
            # gets all the text before the opening delimiter (at start_index)
            before_text = text[:start_index]

            # gets the text between the delimiters, without the delimiters themselves
            # starts at [start_index + len(delimiter)] (inclusive)
            # ends at [end_index] (exclusive)
            delimiter_text = text[start_index + len(delimiter):end_index]

            # remaining text for the next iteration
            # extract all text starting from index [end_index + len(delimiter)] 
            text =  text[end_index + len(delimiter):]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(delimiter_text, text_type))
        # add any remaining text after the delimiters have been processed.
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

"""
    Takes raw markdown text and return a list of tuples
    eg.
    "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    becomes:
    [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
"""
def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

"""
    old node:

    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    returns:

    new_nodes = split_nodes_link([node])
    # [
    #     TextNode("This is text with a link ", TextType.TEXT),
    #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #     TextNode(" and ", TextType.TEXT),
    #     TextNode(
    #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #     ),
    # ] 
"""
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            # if not a text node we just add it to our results unchanged
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            # no image found, append the old node and move on
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text

        for alt_text, url in images:
            # find the image markdown in remaining text
            image_markdown = f"![{alt_text}]({url})"
            # the '1' is to make sure it splits only at the first occurence
            parts = remaining_text.split(image_markdown, 1)

            # add text before the image if it's not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # update the remaining text for the next iteration
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        # add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for alt_text, url in links:
            link_markdown = f"[{alt_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes