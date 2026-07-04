import unittest
from textnode import *
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_1(self):
        node = HTMLNode(props={})
        node2 = HTMLNode()
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    
    def test_2(self):
        node1 = HTMLNode()
        node2 = HTMLNode(tag="html")
        node3 = HTMLNode(value="value")
        node4 = HTMLNode(children=[node1, node2, node3])
        node5 = HTMLNode(props={"href": "http://www.boot.dev"})

    
    def test_3(self):
        node = HTMLNode("p","paragraph")
        node2 = HTMLNode("p","paragraph")
        self.assertEqual(node, node2)

    
    def test_4(self):
        node = HTMLNode("html")
        node2 = HTMLNode("p")
        self.assertNotEqual(node, node2)

    
    
    def test_leaf_to_html_1(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    
    def test_leaf_to_html_2(self):
        node = LeafNode("a", "Hello, world!", {"href": "www.dot.com"})
        self.assertEqual(node.to_html(), '<a href="www.dot.com">Hello, world!</a>')

    
    def test_leaf_to_html_3(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")



    def test_parent_to_html_1(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    
    def test_parent_to_html_2(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    
    def test_parent_to_html_3(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node, grandchild_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><b>grandchild</b><span><b>grandchild</b></span></div>",
        )

    
    def test_parent_to_html_4(self):
        grandchild_node = LeafNode("b", "grandchild", {"color": "red"})
        child_node = ParentNode("span", [grandchild_node], {"color": "yellow"})
        parent_node = ParentNode("div", [child_node], {"color": "blue"})
        self.assertEqual(
            parent_node.to_html(),
            '<div color="blue"><span color="yellow"><b color="red">grandchild</b></span></div>',
        )

    
    def test_parent_to_html_5(self):
        child_node = LeafNode(None, "child", {"color": "yellow"})
        parent_node = ParentNode("div", [child_node], {"color": "blue"})
        self.assertEqual(
            parent_node.to_html(),
            '<div color="blue">child</div>',
        )



    def test_convert_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    
    def test_convert_2(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    
    def test_convert_3(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    
    def test_convert_4(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    
    def test_convert_5(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    
    def test_convert_6(self):
        node = TextNode("This is a link", TextType.LINK, "www.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "www.link"})

    
    def test_convert_7(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.image", "alt": "This is an image"})


if __name__ == "__main__":
    unittest.main()