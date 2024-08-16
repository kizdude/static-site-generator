import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
from inline_processing import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestInlineProcessing(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is text with no delimiters", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_nodes = [
            TextNode("This is text with no delimiters", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        correct_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_italics(self):
        node = TextNode("This is text with a *italics block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        correct_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italics block", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_italics_and_bold(self):
        node = TextNode("This is text with a **italics block** and *bold block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_italic)
        newer_nodes = split_nodes_delimiter(new_nodes, "*", text_type_bold)
        correct_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italics block", text_type_italic),
            TextNode(" and ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(newer_nodes, correct_nodes)

    def test_code_with_bold(self):
        node = TextNode("This is text with a `code block` word and *bold*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word and *bold*", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        correct_images=  [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(images, correct_images)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        correct_links=  [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(links, correct_links)

    def test_extract_no_links(self):
        text = "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        links = extract_markdown_links(text)
        correct_links = []
        self.assertEqual(links, correct_links)

    def test_extract_links_and_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        links = extract_markdown_links(text)
        correct_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(links, correct_links)

    def test_extract_images_and_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        correct_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(images, correct_images)

    def test_extract_no_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        images = extract_markdown_images(text)
        correct_images = []
        self.assertEqual(images, correct_images)

    def test_split_nodes_link(self):
        link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
        )
        new_nodes = split_nodes_link([link_node])
        correct_nodes = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_nodes_link_and_image(self):
        node = TextNode(
        "This is text with an image ![to boot dev](https://www.boot.dev/meme.gif) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        correct_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev/meme.gif"),
            TextNode(" and ", text_type_text),
            TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_nodes_link_and_double_image(self):
        node = TextNode(
        "This is text with an image ![to boot dev](https://www.boot.dev/meme.gif)![2 to boot dev](https://www.boot.dev/2_meme.gif) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        correct_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev/meme.gif"),
            TextNode("2 to boot dev", text_type_image, "https://www.boot.dev/2_meme.gif"),
            TextNode(" and ", text_type_text),
            TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_nodes_no_link(self):
        node = TextNode(
        "This is text with an image ![to boot dev](https://www.boot.dev/meme.gif) and ![2 to boot dev](https://www.boot.dev/2_meme.gif)",
        text_type_text,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        correct_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev/meme.gif"),
            TextNode(" and ", text_type_text),
            TextNode("2 to boot dev", text_type_image, "https://www.boot.dev/2_meme.gif"),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_nodes_no_image(self):
        node = TextNode(
        "This is text with an image [to boot dev](https://www.boot.dev/meme.gif) and [2 to boot dev](https://www.boot.dev/2_meme.gif)",
        text_type_text,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        correct_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev/meme.gif"),
            TextNode(" and ", text_type_text),
            TextNode("2 to boot dev", text_type_link, "https://www.boot.dev/2_meme.gif"),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_nodes_image_empty(self):
        new_nodes = split_nodes_image([])
        new_nodes = split_nodes_link(new_nodes)
        correct_nodes = []
        self.assertEqual(new_nodes, correct_nodes)

    def test_extract_image(self):
        node_image = TextNode(
            "1 Must be text ![2 must be image](https://www.image.com/meme.gif) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text, None
        )
        new_nodes = split_nodes_image([node_image])
        correct_nodes = [
            TextNode("1 Must be text ", text_type_text),
            TextNode("2 must be image", text_type_image, "https://www.image.com/meme.gif"),
            TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_extract_link(self):
        node_link = TextNode(
            "1 Must be text [2 must be link](https://www.link.com) 3 must be text [4 must be link](https://www.link.com)small_text[5 must be link](https://www.link.com)",
            text_type_text
        )
        new_nodes = split_nodes_link([node_link])
        correct_nodes = [
            TextNode("1 Must be text ", text_type_text),
            TextNode("2 must be link", text_type_link, "https://www.link.com"),
            TextNode(" 3 must be text ", text_type_text),
            TextNode("4 must be link", text_type_link, "https://www.link.com"),
            TextNode("small_text", text_type_text),
            TextNode("5 must be link", text_type_link, "https://www.link.com"),
        ]
        self.assertEqual(new_nodes, correct_nodes)


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        correct_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(nodes, correct_nodes)

    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        correct_nodes = []
        self.assertEqual(nodes, correct_nodes)



if __name__ == "__main__":
    unittest.main()