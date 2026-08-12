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

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
    # This is heading

    text in a p

    ## This is another heading with _italic_ text and `code` here

    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is heading</h1><p>text in a p</p><h2>This is another heading with <i>italic</i> text and <code>code</code> here</h2></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """
    # Below is a quote

    > To live is to love
    > To love is to oink
    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Below is a quote</h1><blockquote>To live is to love To love is to oink</blockquote></div>",
        )

    def test_unorderedlist(self):
        md = """
    # Below is an unordered list

    - To live is to love
    - To love is to oink
    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Below is an unordered list</h1><ul><li>To live is to love</li><li>To love is to oink</li></ul></div>",
        )

    def test_orderedlist(self):
        md = """
    # Below is an ordered list

    1. To live is to love
    2. To love is to oink
    """

        node = block_conversion_helpers.markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Below is an ordered list</h1><ol><li>To live is to love</li><li>To love is to oink</li></ol></div>",
        )