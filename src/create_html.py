from htmlnode import HTMLNode, ParentNode

from block_processing import markdown_to_blocks, block_to_block_type, block_type_paragraph, block_type_heading, block_type_code, block_type_quote, block_type_ordered_list, block_type_unordered_list
from inline_processing import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = create_node(block, block_type)
        children_nodes.append(block_node)
    parent = ParentNode("div", children_nodes, None)
    return parent

def create_node(block, block_type):
    tags, values = block_to_tags_and_values(block, block_type)
    # heading
    if block_type == block_type_heading:
        html_block_node = HTMLNode(tags[0], values[0])
    # code
    if block_type == block_type_code:
        code_node = HTMLNode(tags[0], values[0])
        html_block_node = HTMLNode("pre", None, code_node)
    # quote
    if block_type == block_type_quote:
        html_block_node = HTMLNode(tags[0], values[0])
    # ul
    if block_type == block_type_unordered_list:
        html_block_node = list_block_to_htmlnode(block_type_unordered_list, values)
    # ol
    if block_type == block_type_ordered_list:
        html_block_node = list_block_to_htmlnode(block_type_ordered_list, values)
    # paragraph
    if block_type == block_type_paragraph:
        html_block_node = text_block_to_htmlnode(block, block_type_paragraph)

    return html_block_node

def list_block_to_htmlnode(block_type, values):
    children_list_html_nodes = []
    for i in range(len(values)):
        children_list_item_html_nodes = []
        child_list_node = values[i]
        child_list_text_nodes = text_to_textnodes(child_list_node)
        for child_list_text_node in child_list_text_nodes:
            child_list_html_node = text_node_to_html_node(child_list_text_node)
            children_list_item_html_nodes.append(child_list_html_node)
        child_html_node = ParentNode("li", children_list_item_html_nodes)
        children_list_html_nodes.append(child_html_node)

    if block_type == block_type_unordered_list:
        html_block_node = ParentNode("ul", children_list_html_nodes)
    elif block_type == block_type_ordered_list: 
        html_block_node = ParentNode("ol", children_list_html_nodes)
    return html_block_node

def text_block_to_htmlnode(block, block_type):
    if block_type == block_type_paragraph:
        children_html_nodes = []
        children_text_nodes = text_to_textnodes(block) 
        for child_text_node in children_text_nodes:
            child_html_node = text_node_to_html_node(child_text_node)
            children_html_nodes.append(child_html_node)
        html_block_node = ParentNode("p", children_html_nodes)
      
    return html_block_node


def block_to_tags_and_values(block: str, block_type):
    tags = []
    values = []
    # heading
    if block_type == block_type_heading:
        # identify type of heading
        heading = block.split(" ", 1)[0]
        text = block.split(" ", 1)[1]
        heading_type = heading.count("#", 0)
        tag = f"h{heading_type}"
        # separate text from prefix
        tags = [tag]
        values = [text]
        return tags, values
    # code
    if block_type == block_type_code:
        # extract text
        text = block[3:-3]
        tag = f"code"
        tags = [tag]
        values = [text]
        return tags, values
    # quote
    if block_type == block_type_quote:
        tags = []
        values = []
        # extract text
        text = block[1:].strip()
        tag = f"blockquote"
        tags = [tag]
        values = [text]
        return tags, values

    # unordered list
    if block_type == block_type_unordered_list:
        tags = []
        values = []
        lines = block.split("\n")
        for line in lines:
            text = line.split(" ", 1)[1]
            values.append(text)
            tags.append("li")
        return tags, values
    # ordered list
    if block_type == block_type_ordered_list:
        tags = []
        values = []
        lines = block.split("\n")
        for line in lines:
            text = line.split(" ", 1)[1]
            values.append(text)
            tags.append("li")
        return tags, values

    return None, None
