from src.models.textnode import TextNode
from src.models.textnode import TextType

def main():
    line = TextNode("hey", TextType.TEXT, None)
    print(line)
main()