import unittest
import src.helpers.block_conversion_helpers as block_conversion_helpers

class TestBlockHelpers(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = block_conversion_helpers.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_2(self):
        md = """
# This is a Heading

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

## This is the subheading

- This is a list
- with items
"""
        blocks = block_conversion_helpers.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a Heading",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "## This is the subheading",
                "- This is a list\n- with items",
            ],
        )