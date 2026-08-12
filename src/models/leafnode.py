from models.htmlnode import HTMLNode
from typing import Union

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag: str, 
                 value: str, 
                 props: Union[dict[str, str], None] = None):
        self.tag = tag
        self.value = value
        self.props = props
        super(LeafNode, self)

    def __repr__(self):
            return f"HTMLNode({self.tag}, {self.value}, {self.props})"
        
        
    def to_html(self):
        '''
        commenting this out for <link href="www.example.com"></link>
        if not self.value:
            raise ValueError("Leaf Nodes must have value")
        '''
        if not self.tag:
            return self.value
        prop_string = self.props_to_html() if self.props else ""
        value_string = self.value if self.value else ""
        return f"<{self.tag}{prop_string}>{value_string}</{self.tag}>"

    



    