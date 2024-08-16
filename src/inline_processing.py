import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax")
        sub_strings = text.split(delimiter)
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        for i in range(len(sub_strings)):
            if i % 2 == 0:
                new_node = TextNode(sub_strings[i], text_type_text)
            else:
                new_node = TextNode(sub_strings[i], text_type)
            if new_node.text != "":
                new_nodes.append(new_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        images_data = extract_markdown_images(text)
        if len(images_data) == 0:
            new_nodes.append(node)
        for i in range(len(images_data)):
            sub_strings = text.split(f"![{images_data[i][0]}]({images_data[i][1]})", 1)
            new_node = None
            if len(sub_strings) == 1:
                new_node = TextNode(sub_strings[0], text_type_text)
                if new_node.text != "":
                    new_nodes.append(new_node)
            front_node = TextNode(sub_strings[0], text_type_text)
            image_node = TextNode(images_data[i][0], text_type_image, images_data[i][1])
            node_list = [front_node, image_node]
            for n in node_list:
                if n.text == "":
                    node_list.remove(n)
            new_nodes.extend(node_list)
            if len(images_data) - 1 == i:
                last_node = TextNode(sub_strings[1], text_type_text)
                if last_node.text == "":
                    continue
                new_nodes.append(last_node)
            text = sub_strings[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if node.text_type == text_type_image:
            new_nodes.append(node)
            continue
        links_data = extract_markdown_links(text)
        if len(links_data) == 0:
            new_nodes.append(node)
        for i in range(len(links_data)):
            sub_strings = text.split(f"[{links_data[i][0]}]({links_data[i][1]})", 1)
            new_node = None
            if len(sub_strings) == 1:
                new_node = TextNode(sub_strings[0], text_type_text)
                if new_node.text != "":
                    new_nodes.append(new_node)
            front_node = TextNode(sub_strings[0], text_type_text)
            link_node = TextNode(links_data[i][0], text_type_link, links_data[i][1])
            node_list = [front_node, link_node]
            for n in node_list:
                if n.text == "":
                    node_list.remove(n)
            new_nodes.extend(node_list)
            if len(links_data) - 1 == i:
                last_node = TextNode(sub_strings[1], text_type_text)
                if last_node.text == "":
                    continue
                new_nodes.append(last_node)
            text = sub_strings[1]
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"\!\[(.+?)\]\((\S+?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[(.+?)\]\((\S+?)\)", text)
    return links

def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    node_list = [text_node]
    node_images = split_nodes_image(node_list)
    node_links = split_nodes_link(node_images)
    node_bold = split_nodes_delimiter(node_links, "**", text_type_bold)
    node_italics = split_nodes_delimiter(node_bold, "*", text_type_italic)
    node_code = split_nodes_delimiter(node_italics, "`", text_type_code)
    text_nodes_final = node_code
    return text_nodes_final


