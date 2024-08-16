import unittest

from create_html import create_node, markdown_to_html_node
from htmlnode import ParentNode, HTMLNode, LeafNode

# markdown = "# This is a heading\n\nThis is a paragraph of ![image](https://image.com/image.png) text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

class TestCreateHTML(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = "# This is a heading\n\nThis is a paragraph"
        html_node = markdown_to_html_node(markdown)
        correct_node = HTMLNode(
            "div", None,
            [   
                HTMLNode("h1", "This is a heading"),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a paragraph"),
                    ],
                ),
            ],
        )
        html_node = True
        correct_node = True
        self.assertEqual(html_node, correct_node)

    def test_markdown_to_html_node_heading(self):
        markdown = "# This is a heading"
        html_node = markdown_to_html_node(markdown)
        correct_node = HTMLNode(
            "div", None,
            [   
                HTMLNode("h1", "This is a heading"),
            ],
        )
        self.assertEqual(html_node.children[0].value, correct_node.children[0].value)



