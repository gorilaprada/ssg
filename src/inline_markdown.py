import re
from textnode import TextNode, TextType


def text_to_text_nodes(text: str) -> list[TextNode]:
    origin_node = TextNode(text, TextType.TEXT)
    first = split_nodes_image([origin_node])
    second = split_nodes_link(first)
    third = split_nodes_delimiter(second, "**", TextType.BOLD)
    fourth = split_nodes_delimiter(third, "_", TextType.ITALIC)
    fifth = split_nodes_delimiter(fourth, "`", TextType.CODE)
    return fifth

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        elif node.text.count(str(delimiter)) % 2 != 0:
            raise Exception("Invalid MD syntax: delimiter does not have a match")
        list_of_split_str = node.text.split(str(delimiter))
        for i in range(0, len(list_of_split_str)):
            if list_of_split_str[i] == "":
                continue
            elif i == 0 or i % 2 == 0:
                new_node = TextNode(list_of_split_str[i], TextType.TEXT)
            else:
                new_node = TextNode(list_of_split_str[i], text_type)
            new_nodes.append(new_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_images(node.text)
        if not links:
            new_nodes.append(node)
            continue
        node_tracker = node.text
        for image_alt, image_link in links:
            list_of_split_str = node_tracker.split(f"![{image_alt}]({image_link})", 1)
            if list_of_split_str[0] != "":
                list_to_extend = [TextNode(list_of_split_str[0], TextType.TEXT), TextNode(image_alt, TextType.IMAGE, image_link)]
                new_nodes.extend(list_to_extend)
            else:
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_tracker = list_of_split_str[1]
        if node_tracker != "":
            new_nodes.append(TextNode(node_tracker, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        node_tracker = node.text
        for link_text, link_url in links:
            list_of_split_str = node_tracker.split(f"[{link_text}]({link_url})", 1)
            if list_of_split_str[0] != "":
                list_to_extend = [TextNode(list_of_split_str[0], TextType.TEXT), TextNode(link_text, TextType.LINK, link_url)]
                new_nodes.extend(list_to_extend)
            else:
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            node_tracker = list_of_split_str[1]
        if node_tracker != "":
            new_nodes.append(TextNode(node_tracker, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


