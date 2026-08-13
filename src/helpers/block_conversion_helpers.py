import re
import helpers.inline_conversion_helpers as inline_conversion_helpers
from constants import BlockType, TextType
from models.htmlnode import HTMLNode
from models.textnode import TextNode
from models.leafnode import LeafNode
from models.parentnode import ParentNode

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    blocks_stripped = map(lambda x: x.strip(), blocks)
    blocks_stripped_no_empty = list(filter(lambda x: x != '', blocks_stripped))
    return blocks_stripped_no_empty

def block_to_blocktype(block: str) -> BlockType:
    regex_heading = r"#{1,6} (.*|\n)"
    regex_code = r"```\n[\s\S]*?```"
    regex_quote = r"(>.*(\r?\n|$))+"
    regex_unordered_list = r"(- .*(\r?\n|$))+"
    regex_ordered_list = r"(\d\. .*(\r?\n|$))+"
    if re.fullmatch(regex_heading, block):
        return BlockType.HEADING
    if re.fullmatch(regex_code, block):
        return BlockType.CODE
    if re.fullmatch(regex_quote, block):
        return BlockType.QUOTE
    if re.fullmatch(regex_unordered_list, block):
        return BlockType.UNORDERED_LIST
    if re.fullmatch(regex_ordered_list, block):
        return BlockType.ORDERED_LIST
    return BlockType.PARGRAPH

def markdown_to_htmlnode(document: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(document)
    child_nodes: list[HTMLNode] = []
    for block in blocks:
        block = re.sub(r"^[ \t]+", "", block, flags=re.MULTILINE)
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.HEADING:
                heading_size, heading_content = heading_tag_content(block)
                children = text_to_children(heading_content)
                if children:
                    html_node = ParentNode(children, f"h{heading_size}")
                else:
                    html_node = LeafNode(f"h{heading_size}", heading_content)
            case BlockType.CODE:
                text_node = TextNode(block[4:-3], TextType.CODE) #[4:-3] gets the text inside ```
                code_node = inline_conversion_helpers.text_node_to_html_node(text_node)
                html_node = ParentNode([code_node], "pre")
            case BlockType.QUOTE:
                quote_tag_text = quote_tag_content(block)
                block_newline_stripped = re.sub(r"\s+", " ", quote_tag_text)
                children = text_to_children(block_newline_stripped)
                if children:
                    html_node = ParentNode(children, "blockquote")
                else:
                    html_node = LeafNode("blockquote", quote_tag_text)
            case BlockType.PARGRAPH:
                block_newline_stripped = re.sub(r"\s+", " ", block)

                children = text_to_children(block_newline_stripped)
                if children:
                    html_node = ParentNode(children, "p")
                else:
                    html_node = LeafNode("p", block_newline_stripped)
            case BlockType.UNORDERED_LIST:
                unordered_list_items: list[HTMLNode] = list_children(block, BlockType.UNORDERED_LIST)
                unordered_list_items_modified: list[HTMLNode] = []
                for item in unordered_list_items:
                    text = item.value
                    children = text_to_children(text)
                    if children:
                        unordered_list_items_modified.append(ParentNode(children, item.tag))
                    else:
                        unordered_list_items_modified.append(LeafNode(item.tag, item.value))
                html_node = ParentNode(unordered_list_items_modified, "ul")
            case BlockType.ORDERED_LIST:
                ordered_list_items: list[HTMLNode] = list_children(block, BlockType.ORDERED_LIST)
                ordered_list_items_modified: list[HTMLNode] = []
                for item in ordered_list_items:
                    text = item.value
                    children = text_to_children(text)
                    if children:
                        ordered_list_items_modified.append(ParentNode(children, item.tag))
                    else:
                        ordered_list_items_modified.append(LeafNode(item.tag, item.value))
                html_node = ParentNode(ordered_list_items_modified, "ol")
        child_nodes.append(html_node)
    return ParentNode(child_nodes, "div")

# markdown_to_htmlnode helpers
def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = inline_conversion_helpers.text_to_textnodes(text)
    children: list[HTMLNode] = []
    for text_node in text_nodes:
        child_node = inline_conversion_helpers.text_node_to_html_node(text_node)
        children.append(child_node)
    return children


def list_children(md: str, list_type: BlockType) -> list[HTMLNode]:
    '''
    takes input like:
    - one
    - two
    and returns 
    [
        HtmlNode('li', 'one'),
        HtmlNode('li', 'two')
    ]
    '''
    child_nodes: list[HTMLNode] = []
    list_items: list[str] = md.split('\n')
    if list_type == BlockType.UNORDERED_LIST:
        index = 2
    elif list_type == BlockType.ORDERED_LIST:
        index = 3
    for list_item in list_items:
        child_nodes.append(LeafNode("li", list_item[index:]))
    return child_nodes

def quote_tag_content(quote_md: str) -> str:
    '''
    takes an input string like:
    > one\n>two\n> three
    and returns string like
    one\ntwo\nthree
    '''
    quotes = quote_md.split('\n')
    quotes_without_md_tag = []
    for quote in quotes:
        if len(quote) < 2:
            continue
        if quote[1] == ' ':
            quotes_without_md_tag.append(quote[2:])
            continue
        quotes_without_md_tag.append(quote[1:])
    return '\n'.join(quotes_without_md_tag)

def heading_tag_content(heading_md: str) -> (str, str):
    [heading_tag, heading_content] = heading_md.split(' ', maxsplit=1)
    heading_size = len(heading_tag)
    return heading_size, heading_content
    