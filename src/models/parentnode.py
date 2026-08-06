from src.models.htmlnode import HTMLNode
from typing import Union

class ParentNode(HTMLNode):
    def __init__(self,
                 children: list[HTMLNode],
                 tag: Union[str, None] = None,
                 props: Union[dict[str, str], None] = None):
        self.children = children
        self.tag = tag
        self.props = props
        super(HTMLNode, self)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Nodes must have tag")
        if not self.children:
            raise ValueError("Parent Nodes must have children")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        prop_string = self.props_to_html() if self.props else ""
        return f"<{self.tag}{prop_string}>{child_html}</{self.tag}>"


