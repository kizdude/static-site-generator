import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "hello", None, { "href": "https://www.google.com" })
        self.assertEqual(str(node), f"tag: {node.tag}, value: {node.value}, children: {node.children}, props: {node.props}")

    def test_props_to_html(self):
        node = HTMLNode("a", "hello", None, { "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html_empty(self):
        node = HTMLNode("a", "hello", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_node(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")


    def test_leaf_node_props(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_node_no_tag(self):
        leaf_node = LeafNode(None, "This is plain text.")
        self.assertEqual(leaf_node.to_html(), "This is plain text.")

    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_parent_child_to_html(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_no_children_to_html(self):
        node = ParentNode(
            "p", 
        )
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_no_tag_to_html(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()