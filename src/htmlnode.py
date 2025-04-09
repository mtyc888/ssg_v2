class HTMLNode:
    """
        tag - A string represening the HTML tag name (eg. "p", "a", "h1")

        value - A string representing the value of the HTML tag (eg. the text inside a <p> tag)

        children - A list of HTMLNodes objects representing the children of this node

        props - A dictionary of key-value pairs, representing the attributes of the HTML tag.
                for example, a link (<a> tag) might have {"href":"https://www.google.com"}
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props
    """
        Child classes will override this method.
    """
    def to_html(self):
        raise NotImplementedError
    """
        This returns a string that represents the HTML attributes of the node.
        For example this:

            {
                "href": "https://www.google.com",
                "target": "_blank",
            }

            will return this:

            href="https://www.google.com" target="_blank"
    """
    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for key, value in self.props.items():
            string = string + f' {key}="{value}"'
        return string
    """
        This returns a string representation of a HTMLNode.
    """
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
"""
    A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
    eg.
        <p>Hello</p>
"""
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
"""
    Any HTMLNode that is not a LeafNode is a parent node
"""
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node needs a tag")
        if self.children is None:
            raise ValueError("Parent node needs children")
        html_str = f"<{self.tag}>"
        for child in self.children:
            html_str = html_str + child.to_html()
        final_html = html_str + f"</{self.tag}>"
        return final_html
    