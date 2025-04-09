import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """
        This test creates two TextNodes with the same properties and 
        assert them to be Equal.
    """
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    """
        This test creates two TextNodes with the different properties and 
        assert them to be NOT Equal.
    """
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    """
        This test creates two TextNodes with the same properties and 
        take their string representation and compare them if they're Equal.
    """
    def test_repr_(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node_str = node.__repr__()
        node2_str = node2.__repr__()
        self.assertEqual(node_str, node2_str)

if __name__ == "__main__":
    unittest.main()