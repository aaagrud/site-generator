import re
from src.constants import BlockType

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    blocks_stripped = map(lambda x: x.strip(), blocks)
    blocks_stripped_no_empty = list(filter(lambda x: x != '', blocks_stripped))
    return blocks_stripped_no_empty

def block_to_blocktype(block: str) -> BlockType:
    regex_heading = r"#{1,6}"
    regex_code = r"```\n(.*)```"
    regex_quote = r"(>.*(\r?\n|$))+"
    regex_unordered_list = r"(- .*(\r?\n|$))+"
    regex_ordered_list = r"(\d\. .*(\r?\n|$))+"
    if re.match(regex_heading, block):
        return BlockType.HEADING
    if re.match(regex_code, block):
        return BlockType.CODE
    if re.match(regex_quote, block):
        return BlockType.QUOTE
    if re.match(regex_unordered_list, block):
        return BlockType.UNORDERED_LIST
    if re.match(regex_ordered_list, block):
        return BlockType.ORDERED_LIST
    return BlockType.PARGRAPH