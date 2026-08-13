from models.textnode import TextNode
from models.textnode import TextType
from helpers.file_helpers import copy_content_static_to_public_recursive
from helpers.website_generation_helpers import generate_pages_recursive

def main():
    copy_content_static_to_public_recursive('./static', './public')
    generate_pages_recursive('./content', './template.html', './public')
main()