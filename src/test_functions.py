import unittest

from functions import *
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_split_nodes_1(self):
        node = TextNode("**This sentence is bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("This sentence is bold", TextType.BOLD)])

    def test_split_nodes_2(self):
        node = TextNode("This _word_ and this _word_ are _italic_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(nodes, [TextNode("This ", TextType.TEXT),
                                TextNode("word", TextType.ITALIC),
                                TextNode(" and this ", TextType.TEXT),
                                TextNode("word", TextType.ITALIC),
                                TextNode(" are ", TextType.TEXT), 
                                TextNode("italic", TextType.ITALIC)]
                            )
    
    def test_split_nodes_3(self):
        node = TextNode("This sentence is normal", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("This sentence is normal", TextType.TEXT)])

    def test_split_nodes_4(self):
        node = TextNode("`print('hello, world!')` is code", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes, [TextNode("print('hello, world!')", TextType.CODE), TextNode(" is code", TextType.TEXT)])

    def test_split_nodes_5(self):
        node = TextNode("The final word is _italic_", TextType.TEXT)
        node2 = TextNode("**This sentence is bold**", TextType.TEXT)
        node3 = TextNode("**The** first word is bold", TextType.TEXT)
        nodes = split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("The final word is ", TextType.TEXT), TextNode("italic", TextType.ITALIC),
                                TextNode("This sentence is bold", TextType.BOLD),
                                TextNode("The", TextType.BOLD), TextNode(" first word is bold", TextType.TEXT)])

    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://dotcom.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://chess.com) and an ![image](image.image))"
        )
        self.assertListEqual([("link", "https://chess.com")], matches)

    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links(
            "This is text with two [link one](https://link/one.one) [link two](https://link/two.two) links"
        )
        self.assertListEqual([("link one", "https://link/one.one"), ("link two", 'https://link/two.two')], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with two ![image one](https://image/imageone.com) ![image two](https://image/imagetwo.com) images"
        )
        self.assertListEqual([("image one", "https://image/imageone.com"), ("image two", 'https://image/imagetwo.com')], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://imgur.com) and another [second link](https://chess.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://chess.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_none(self):
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_node = split_nodes_image(split_nodes_link([node]))
        self.assertListEqual(
            [
                TextNode("This is text with nothing", TextType.TEXT),
            ],
            new_node,
        )

    def test_split_mult(self):
        node = TextNode(
            "This is text with a [link](https://imgur.com) and another ![image](https://imgur/image.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgur/image.com"
                ),
            ],
            new_nodes,
        )

    
    def test_final(self):
        text_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(text_nodes,
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ] )
    
    def test_final_2(self):
        text_nodes = text_to_textnodes("")
        self.assertEqual(text_nodes,
        [] )

    def test_final_2(self):
        text_nodes = text_to_textnodes("[link](link)![image](link)[link](link)![image](link)")
        self.assertEqual(text_nodes,
        [TextNode('link',TextType.LINK,"link"),
        TextNode('image',TextType.IMAGE,"link"),
        TextNode('link',TextType.LINK,"link"),
        TextNode('image',TextType.IMAGE,"link"),] )

    def test_final_3(self):
        text_nodes = text_to_textnodes("`code`****_italic_``__**bold**")
        self.assertEqual(text_nodes,
        [TextNode("code", TextType.CODE),
        TextNode("italic", TextType.ITALIC),
        TextNode("bold", TextType.BOLD)] )

    def test_final_4(self):
        text_nodes = text_to_textnodes("This is normal text")
        self.assertEqual(text_nodes,
        [TextNode("This is normal text", TextType.TEXT)] )

if __name__ == "__main__":
    unittest.main()