import unittest
import src.helpers.block_conversion_helpers as block_conversion_helpers
from src.constants import BlockType
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

    def test_block_to_block_type_paragraph(self):
        md = """
"How are you?" is a very common greeting in english. 

"How do you do?" is an old fashioned way of saying the same thing!
"""
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARGRAPH)

    def test_block_to_block_type_heading(self):
        md = "# 'How are you?' is a very common greeting in english."
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = '''```
for i in range(10):
    print(i)```'''
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = '''> oink
>yoink'''
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = '''- oink
- yoink'''
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        md = '''1. oink
2. yoink'''
        block_type = block_conversion_helpers.block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


   