from typing import Union

class HTMLNode():
    def __init__(self, 
                 tag: Union[str, None] = None, 
                 value: Union[str, None] = None,
                 children: Union[list["HTMLNode"], None] = None,
                 props: Union[dict[str, str], None] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_string = ""
        for prop in self.props:
            prop_string += f' {prop}="{self.props[prop]}" '
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
        