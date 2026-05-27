import re
from enum import Enum
# ========================================================== For markdown_to_html
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_text_nodes
# ==========================================================

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_title(markdown: str) -> str:
    list_of_lines = markdown.split("\n")
    for line in list_of_lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header in markdown")

# ==========================================================
# For markdown_to_html

def markdown_to_html_node(markdown: str) -> ParentNode:
    md_split = markdown_to_blocks(markdown)
    list_of_block_nodes = []
    for block in md_split:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            new_html_node = paragraph_to_html_node(block)
            list_of_block_nodes.append(new_html_node)

        elif block_type == BlockType.HEADING:
            new_html_node = heading_to_html_node(block)
            list_of_block_nodes.append(new_html_node)

        elif block_type == BlockType.CODE:
            new_html_node = code_to_html_node(block)
            list_of_block_nodes.append(new_html_node)

        elif block_type == BlockType.QUOTE:
            new_html_node = quote_to_html_node(block)
            list_of_block_nodes.append(new_html_node)

        elif block_type == BlockType.UNORDERED_LIST:
            new_html_node = ulist_to_html_node(block)
            list_of_block_nodes.append(new_html_node)

        elif block_type == BlockType.ORDERED_LIST:
            new_html_node = olist_to_html_node(block)
            list_of_block_nodes.append(new_html_node)
    final_html_node = ParentNode("div", list_of_block_nodes)
    return final_html_node

def paragraph_to_html_node(block:str) -> ParentNode:
    cleaned_block = block.replace("\n", " ")
    children = text_to_children(cleaned_block)
    new_html_node = ParentNode("p", children)
    return new_html_node

def heading_to_html_node(block: str) -> ParentNode:
    block_parts = block.split(" ", 1)
    heading_level = len(block_parts[0])
    heading_text = block_parts[1]
    children = text_to_children(heading_text)
    new_html_node = ParentNode(f"h{heading_level}", children)
    return new_html_node

def code_to_html_node(block: str) -> ParentNode:
    cleaned_block = block.removeprefix("```\n").removesuffix("```")
    code_html_node = LeafNode("code", cleaned_block)
    new_html_node = ParentNode("pre", [code_html_node])
    return new_html_node

def quote_to_html_node(block: str) -> ParentNode:
    cleaned_block = " ".join([line.removeprefix("> ").removeprefix(">") for line in block.split("\n")])
    children = text_to_children(cleaned_block)
    new_html_node = ParentNode("blockquote", children)
    return new_html_node

def ulist_to_html_node(block: str) -> ParentNode:
    list_of_cleaned_lines= [line.removeprefix("- ") for line in block.split("\n")]
    outer_children = []
    for line in list_of_cleaned_lines:
        inner_children = text_to_children(line)
        inner_new_html_node = ParentNode("li", inner_children)
        outer_children.append(inner_new_html_node)
    new_html_node = ParentNode("ul", outer_children)
    return new_html_node

def olist_to_html_node(block: str) -> ParentNode:
    list_of_lines = block.split("\n")
    list_of_cleaned_lines= [line.removeprefix(f"{i}. ") for i, line in enumerate(list_of_lines, 1)]
    outer_children = []
    for line in list_of_cleaned_lines:
        inner_children = text_to_children(line)
        inner_new_html_node = ParentNode("li", inner_children)
        outer_children.append(inner_new_html_node)
    new_html_node = ParentNode("ol", outer_children)
    return new_html_node

def text_to_children(block: str) -> list[HTMLNode]:
    list_of_new_html_nodes = []
    list_of_text_nodes = text_to_text_nodes(block)
    for text_node in list_of_text_nodes:
        list_of_new_html_nodes.append(text_node_to_html_node(text_node))
    return list_of_new_html_nodes


# ==========================================================

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.match(r"^```\n.*```$", block, re.DOTALL):
        return BlockType.CODE
    if re.match(r"^(>.*\n?)+$", block, re.MULTILINE):
        return BlockType.QUOTE
    if re.match(r"^(- .*\n?)+$", block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    lines = block.split("\n")
    pattern = "".join(rf"^{i}\. .+\n?" for i, _ in enumerate(lines, 1))
    if re.match(pattern, block, re.MULTILINE):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    return [text.strip() for text in split_markdown if text != ""]

