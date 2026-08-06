from enum import Enum

class TextType(Enum):
    ITALICS = "italics"
    BOLD = "bold"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"
    CODE = "code"

class BlockType(Enum):
    PARGRAPH = "paragraph"
    HEADING = "heading" 
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE = "code"