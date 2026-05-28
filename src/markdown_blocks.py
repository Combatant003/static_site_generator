from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]


def heading_level(block):
    count = 0
    for ch in block:
        if ch == "#":
            count += 1
        else:
            break
    return count


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        text = " ".join(block.split("\n"))
        return ParentNode("p", text_to_children(text))

    if block_type == BlockType.HEADING:
        level = heading_level(block)
        text = block[level + 1:]
        return ParentNode(f"h{level}", text_to_children(text))

    if block_type == BlockType.CODE:
        content = block[4:-3]
        code_node = text_node_to_html_node(TextNode(content, TextType.CODE))
        return ParentNode("pre", [code_node])

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped = [line[1:].lstrip(" ") for line in lines]
        text = "\n".join(stripped)
        return ParentNode("blockquote", text_to_children(text))

    if block_type == BlockType.UNORDERED_LIST:
        items = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in block.split("\n"):
            text = line.split(". ", 1)[1]
            items.append(ParentNode("li", text_to_children(text)))
        return ParentNode("ol", items)

    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
