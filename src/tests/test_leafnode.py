import unittest
from src.models.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Image", {"href": "www.image.com"})
        self.assertEqual(node.to_html(), '<a href="www.image.com" >Image</a>')

    def test_leaf_to_html_link(self):
            node = LeafNode("link", None, {"href": "/styles.css"})
            self.assertEqual(node.to_html(), '<link href="/styles.css" ></link>')
