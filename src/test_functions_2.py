import unittest
from functions_2 import *

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_2(self):
        md = """

        This is a block.
Words.
More words. 

    This is another block.
This is a continuation of the last block.  


    This is the final block.   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block.\nWords.\nMore words.",
                "This is another block.\nThis is a continuation of the last block.",
                "This is the final block.",
            ],
        )

    def test_markdown_to_blocks_3(self):
        md = """
  
 
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    
    
    def test_block_to_block_type(self):
            md = """
# This is a heading.

This is a normal paragraph.
Nothing special about it

```
This is code
```

- This
- Is An
- Unordered List

1. This List
2. Is Ordered

> This is a quote
"""
            types = [block_to_block_type(block) for block in markdown_to_blocks(md)]
            self.assertEqual(
                types, [BlockType.H, BlockType.P, BlockType.C, BlockType.UL, BlockType.OL, BlockType.Q])

    def test_block_to_block_type(self):
            md = """
This is not a heading

- 
-This is not an ordered list

- 
- This is

1. 
2. 
4. This is not an ordered list

1. 
2. 
3. This is 

>This is a quote
> And this is a quote
"""
            types = [block_to_block_type(block) for block in markdown_to_blocks(md)]
            self.assertEqual(
                types, [BlockType.P, BlockType.P, BlockType.UL, BlockType.P, BlockType.OL, BlockType.Q])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_lists(self):
        md = """
- One
- Two
- Three

1. One
2. Two
3. Three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>One</li><li>Two</li><li>Three</li></ul><ol><li>One</li><li>Two</li><li>Three</li></ol></div>",
        )

    def test_headings(self):
        md = """
# One

## Two

### Three

#### Four

##### Five

###### Six
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>One</h1><h2>Two</h2><h3>Three</h3><h4>Four</h4><h5>Five</h5><h6>Six</h6></div>",
        )



if __name__ == "__main__":
    unittest.main()