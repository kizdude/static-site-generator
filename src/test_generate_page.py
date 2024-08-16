import unittest

from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a heading"
        title = extract_title(markdown)
        correct_title = "This is a heading"
        self.assertEqual(title, correct_title)

    def test_extract_title_err(self):
        markdown = " This is a heading"
        self.assertRaises(Exception, extract_title, markdown)

    def test_extract_title_nested(self):
        markdown = "```code```\n\n# This is a heading\n\n>quote"
        title = extract_title(markdown)
        correct_title = "This is a heading"
        self.assertEqual(title, correct_title)