import sys
from models.textnode import TextNode
from models.textnode import TextType
from helpers.file_helpers import copy_content_static_to_public_recursive
from helpers.website_generation_helpers import generate_pages_recursive

def main(args):
    base_path = args[0] if args else '/'
    copy_content_static_to_public_recursive('./static', './docs')
    generate_pages_recursive('./content', './template.html', './docs', base_path)

main(sys.argv)