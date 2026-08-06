import unittest
import src.helpers.inline_conversion_helpers as inline_conversion_helpers
from src.models.textnode import TextNode, TextType

class TestHelpers(unittest.TestCase):
    def test_italics(self):
        nodes: list[TextNode] =[TextNode("Hello _bestie_!", TextType.TEXT)]
        split_nodes: list[TextNode] = inline_conversion_helpers.split_nodes_delimiter(nodes, '_', TextType.ITALICS)
        expected_nodes_list: list[TextNode] = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bestie", TextType.ITALICS),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(split_nodes, expected_nodes_list)

    def test_extract_markdown_images(self):
        matches = inline_conversion_helpers.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = inline_conversion_helpers.extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_2_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ)!",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        ) 

    def test_split_single_link_with_bold(self):
        node = TextNode(
            "This is **text** with a [link](https://i.imgur.com/zjjcJKZ)!",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is **text** with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_2_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_single_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)!",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_single_images_with_bold(self):
        node = TextNode(
            "This is **text** with an ![image](https://i.imgur.com/zjjcJKZ.png)!",
            TextType.TEXT,
        )
        new_nodes = inline_conversion_helpers.split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is **text** with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALICS),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ] 
        self.assertEqual(expected_output, inline_conversion_helpers.text_to_textnodes(text)) 