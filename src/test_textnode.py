import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", "italic")
        self.assertEqual(node.url, None)

    def test_url(self):
        node = TextNode("This is a text node", "link", "https://boot.dev")
        self.assertEqual(node.url, "https://boot.dev")

    def test_italic_text_node_to_html(self):
        text_node = TextNode("This is a text node", "italic")
        html_node = text_node_to_html_node(text_node)
        to_html = html_node.to_html()
        self.assertEqual(to_html, "<i>This is a text node</i>")

    def test_link_text_node_to_html(self):
        text_node = TextNode("This is a link node", "link", "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        to_html = html_node.to_html()
        self.assertEqual(to_html, "<a href=\"https://boot.dev\">This is a link node</a>")

    def test_image_text_node_to_html(self):
        text_node = TextNode("Alt text", "image", "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        to_html = html_node.to_html()
        self.assertEqual(to_html, "<img src=\"https://boot.dev\" alt=\"Alt text\"></img>")

    def test_text_node_to_html_error(self):
        text_node = TextNode("Alt text", "not real", "https://boot.dev")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)


if __name__ == "__main__":
    unittest.main()