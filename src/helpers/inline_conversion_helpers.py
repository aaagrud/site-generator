import re
from models.textnode import TextType, TextNode
from models.leafnode import LeafNode

def text_node_to_html_node(textnode: "TextNode"):
    match textnode.type:
        case TextType.ITALICS:
            return LeafNode("i", textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.IMAGE:
            return LeafNode("img", textnode.text, {"src": f"{textnode.url}", "alt": f"{textnode.text}"})
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": f"{textnode.url}"})
        case TextType.CODE:
            return LeafNode("code", textnode.text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    '''
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    returns
    [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
    ]
    '''
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Closing delimiter not found")
        for i, part in enumerate(parts):
            if parts[i] == '':
                continue
            # odd items are text nodes, even items are italics, bold or code
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    '''
    node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
            "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
        ),
    ]    
    '''
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        to_parse = old_node.text
        for link in links:
            link_text = link[0]
            link_url = link[1]
            before, remaining = to_parse.split(f"[{link_text}]({link_url})", maxsplit = 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            to_parse = remaining
        if to_parse:
            new_nodes.append(TextNode(to_parse, TextType.TEXT))
    return new_nodes

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    '''
    node = TextNode(
    "This is text with a image ![to boot dev](https://www.boot.dev/img) and ![to youtube image](https://www.youtube.com/@bootdotdev/image)",
    TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/img"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
            "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev/image"
        ),
    ]    
    '''
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        to_parse = old_node.text
        for image in images:
            image_text = image[0]
            image_url = image[1]
            before, remaining = to_parse.split(f"![{image_text}]({image_url})", maxsplit = 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            to_parse = remaining
        if to_parse:
            new_nodes.append(TextNode(to_parse, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str):
    '''
    example input: 
    This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

    example output:
    [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ] 
    '''
    text_node = TextNode(text, TextType.TEXT)
    delimited_nodes_code = split_nodes_delimiter([text_node], '`', TextType.CODE)
    delimited_nodes_italics = split_nodes_delimiter(delimited_nodes_code, '_', TextType.ITALICS)
    delimited_nodes_bold = split_nodes_delimiter(delimited_nodes_italics, '**', TextType.BOLD) 
    return split_nodes_link(split_nodes_images(delimited_nodes_bold))

# helpers for above functions split_nodes_link and split_nod
def extract_markdown_images(text: str):
    '''
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    '''
    markdown_image_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(markdown_image_regex, text)

def extract_markdown_links(text: str):
    '''
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    '''

    markdown_link_regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(markdown_link_regex, text)