import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(
            TextNode("This is a text node", TextType.BOLD), 
            TextNode("This is a text node", TextType.BOLD))

    def test_type(self):
        self.assertNotEqual(
            TextNode("This is a text node", TextType.LINK, "This is a link"),
            TextNode("This is a text node",TextType.IMAGE,"This is a link"))

    def test_links(self):
        self.assertNotEqual(
            TextNode("This is a text node", TextType.TEXT, "This is a link"),
            TextNode("This is a text node",TextType.TEXT))

    def test_text(self):
        self.assertNotEqual(
            TextNode("This is a text node", TextType.TEXT), 
            TextNode("This is not a text node",TextType.TEXT))

if __name__ == "__main__":
    unittest.main()