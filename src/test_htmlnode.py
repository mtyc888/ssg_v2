import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType

class TestHTMLNode(unittest.TestCase):
    """
        This test creates a HTML node and test the props_to_html function
    """
    def test_props_to_html_simple(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    """
        This test creates a HTML node and test the props_to_html function with
        multiple properties
    """
    def test_multiple_props(self):
        node = HTMLNode("a", "This is a test", None, {
            "href":"https://example.com",
            "target":"_blank"
        })
        self.assertIn(' href="https://example.com"', node.props_to_html())
        self.assertIn(' target="_blank"', node.props_to_html())
        self.assertEqual(len(node.props_to_html()), len(' href="https://example.com" target="_blank"'))
        
    """
        This test creates a HTML node and test props_to_html with None props
    """
    def test_none_props(self):
        node = HTMLNode("p", "This is a test", None, None)
        self.assertEqual(node.props_to_html(), "")
    """
        This test creates a HTML node and test props_to_html with empty props
    """
    def test_empty_props(self):
        node = HTMLNode("p", "test", None, {})
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    """
        This test creates a LeafNode and test to_html() function
    """
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, World!")
        node2 = LeafNode("h1", "THIS IS A TEST")
        self.assertEqual(node2.to_html(), "<h1>THIS IS A TEST</h1>")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

class TestParentNode(unittest.TestCase):
    """
        This test creates a ParentNode and a LeafNode to see if the
        to_html() function returns the correct HTML code.
    """
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    """
        This test creates 2 ParentNodes and 1 LeafNode, 1 parent within another parent, 
        then 1 leaf node within the inner parent node. 

        And we test if the to_html outputs the correct HTML code.
    """
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class TestTextNode(unittest.TestCase):
    """
        This test creates a TextNode to test the text_node_to_html_node() function,
        to convert the TextNode into HTMLNode, specifically a LeafNode
    """
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    