from textnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Format Section Not Closed")
    
        split_nodes = []
        index = 2
        for text in split_text:
            if text and index % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            elif text:
                split_nodes.append(TextNode(text, text_type))
            index += 1 
        
        new_nodes.extend(split_nodes)
    
    return new_nodes


import re

def extract_markdown_images(text):
    images = re.findall(r"\!\[.*?\]\(.*?\)", text)
    tuples = []
    for image in images:
        alt_text = re.findall(r"\!\[.*?\]\(", image)[0][2:-2]
        link_text = re.findall(r"\]\(.*?\)", image)[0][2:-1]
        tuples.append((alt_text, link_text))
    return tuples

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[.*?\]\(.*?\)", text)
    tuples = []
    for link in links:
        alt_text = re.findall(r"\[.*?\]\(", link)[0][1:-2]
        link_text = re.findall(r"\]\(.*?\)", link)[0][2:-1]
        tuples.append((alt_text, link_text))
    return tuples



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        split = re.sub(r"\!\[.*?\]\(.*?\)", "_i_", old_node.text).split("_")
        
        if len(split) < 2:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        image_nodes = [(TextNode(image[0], TextType.IMAGE, image[1])) for image in images]
        
        final_nodes = []
        i = 0
        
        for text in split:
            if text:
                if text == "i":
                    final_nodes.append(image_nodes[i])
                    i += 1
                else:
                    final_nodes.append(TextNode(text, TextType.TEXT))
        
        new_nodes.extend(final_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        split = re.sub(r"(?<!!)\[.*?\]\(.*?\)","_l_", old_node.text).split("_")
        
        if len(split) < 2:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        
        link_nodes = [(TextNode(link[0], TextType.LINK, link[1])) for link in links]
        final_nodes = []
        i = 0
        for text in split:
            if text:
                if text == "l":
                    final_nodes.append(link_nodes[i])
                    i += 1
                else:
                    final_nodes.append((TextNode(text, TextType.TEXT)))
        
        new_nodes.extend(final_nodes)
    return new_nodes




def text_to_textnodes(text):
    return (
        split_nodes_image(
            split_nodes_link(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter(
                    [TextNode(text, TextType.TEXT)], 
                    "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)
                )
            )
        )