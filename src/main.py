from models.textnode import TextNode
from models.textnode import TextType
from helpers.file_helpers import copy_content_static_to_public

def main():
    line = TextNode("hey", TextType.TEXT, None)
    print(line)
    print(copy_content_static_to_public('./static', './public'))
main()