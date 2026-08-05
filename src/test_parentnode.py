import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_with_child(self):
        node1 = LeafNode("p",
                         "This is a paragraph",
                         None,)
        node2 = ParentNode([node1], "div", None)
        self.assertEqual(node2.to_html(), 
                         "<div><p>This is a paragraph</p></div>")

    def test_nested_parent(self):
       node1 = LeafNode("p",
                        "This is a paragraph",
                        None,)
       node2 = ParentNode([node1], "div", None)
       node3 = ParentNode([node2], "div", {"className": "node3"})
       self.assertEqual(node3.to_html(), 
                        '<div className="node3" ><div><p>This is a paragraph</p></div></div>') 

    def test_multiple_children(self):
       node1 = LeafNode("p",
                        "This is a paragraph",
                        None,)
       node2 = LeafNode("p",
                        "This is a paragraph",
                        None,)
       node3 = ParentNode([node1, node2], "div", {"className": "node3"})
       self.assertEqual(node3.to_html(), 
                        '<div className="node3" ><p>This is a paragraph</p><p>This is a paragraph</p></div>') 

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node1 = ParentNode(None, "p", None)
            node1.to_html()