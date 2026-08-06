from src.models.htmlnode import HTMLNode
import unittest

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        node2 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        node2 = HTMLNode("a", None, None, {"href": "https://www.example2.com"})
        self.assertNotEqual(node1, node2)

    def test_props_to_html(self):
        node1 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        props_string = node1.props_to_html()
        self.assertEqual(props_string, ' href="https://www.example.com" ')
