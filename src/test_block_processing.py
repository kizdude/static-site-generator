import unittest

from block_processing import markdown_to_blocks, block_to_block_type

class TestBlockProcessing(unittest.TestCase):
    def test_block_processing(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(markdown)
        correct_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(blocks, correct_blocks)

    def test_block_processing_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        correct_blocks = []
        self.assertEqual(blocks, correct_blocks)

    def test_block_to_block_type(self):
        blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is first list item\n* This is second list item\n* This is third list item",
            "## This is another heading",
            "This is a paragraph",
            "1. This is first ordered list item\n2. This is second ordered list item\n3. This is third ordered list item",
            "```This is a code block```",
            ">This is first quote item\n>This is second quote item",
            "1. Big List\n2. a\n3. b\n4. c\n5. \n6. d\n7. e\n8. f\n9. g\n10. h\n11. i"
        ]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))

        correct_block_types = ["heading", "paragraph", "unordered_list", "heading", "paragraph", "ordered_list", "code", "quote", "ordered_list"]
        self.assertEqual(block_types, correct_block_types)

