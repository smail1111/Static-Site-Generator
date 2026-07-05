from enum import Enum
from functions import *
from htmlnode import *

def markdown_to_blocks(markdown):
    blocks = []
    current_block = ""
    for line in markdown.split("\n"):
        if line.strip() == "":
            if current_block.strip() != "":
                blocks.append(current_block.strip())
            current_block = ""
        else:
            current_block += line + "\n"
    
    return blocks


class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    C = "code"
    Q = "quote"
    UL = "unorderedlist"
    OL = 'orderedlist'


def block_to_block_type(block):
    lines = block.split("\n")
    
    if len(lines) == 1 and lines[0][0] == "#":
        return BlockType.H
    
    if lines [0] == "```" and lines[-1] == "```":
        return BlockType.C
    
    is_unord_list, is_ord_list, is_quote = True, True, True
    
    i = 1
    for line in lines:
        
        if line[0:2] != "- ":
            is_unord_list = False
        
        if line[0:len(str(i)) + 2] != f"{i}. ":
            is_ord_list = False
        else:
            i += 1
        
        if line[0] != ">":
            is_quote = False
    
    
    if is_unord_list:
        return BlockType.UL
    
    elif is_ord_list:
        return BlockType.OL
    
    elif is_quote:
        return BlockType.Q

    else:
        return BlockType.P



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        match block_to_block_type(block).value:
            case "paragraph":
                block_nodes.append(block_to_htmlnode(block.replace("\n", " "), "p"))
            
            case "heading":
                block_nodes.append(block_to_htmlnode(block.strip("#").strip(), f"h{len(block.split(" ", 1)[0])}"))
            
            case "unorderedlist":
                block_nodes.append(list_to_htmlnode(block, "ul"))

            case "orderedlist":
                block_nodes.append(list_to_htmlnode(block, "ol"))
            
            case "quote":
                block_nodes.append(block_to_htmlnode(block.replace("\n", " ").replace(">", "").strip(), "blockquote"))
            
            case "code":
                block_nodes.append(code_to_htmlnode(block))

    return ParentNode("div", block_nodes)


def block_to_htmlnode(block, tag):
    return ParentNode(tag, [
        text_node_to_html_node(child) for child in text_to_textnodes(block.replace("\n", " "))
        ]
            )


def code_to_htmlnode(block):
    return ParentNode("pre",[(text_node_to_html_node(TextNode(block[4:-4] + "\n", TextType.CODE)))])


def list_to_htmlnode(block, tag):
    lines = block.split("\n")
    items = []
    for line in lines:
        items.append(block_to_htmlnode(line.split(" ", 1)[1], "li"))
    return ParentNode(tag, items)