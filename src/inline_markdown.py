import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # We only look inside and split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text by the targeted delimiter
        parts = node.text.split(delimiter)

        # If there's an even number of elements, it means a closing delimiter is missing
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: matching closing delimiter '{delimiter}' not found in text: '{node.text}'"
            )

        # Walk through the fragments and assign the matching type rules
        for i in range(len(parts)):
            # Skip empty parts (e.g., if delimiter is at the absolute start or end of text)
            if parts[i] == "":
                continue

            if i % 2 == 0:
                # Even index means outside the delimiter (Plain Text)
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # Odd index means inside the delimiter (Target formatting type)
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!\! )\[(.*?)\]\((.*?)\)"
    pattern = r"\[(.*?)\]\((.*?)\)"
    strict_link_pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return re.findall(strict_link_pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        pattern = r"\!\[(.*?)\]\((.*?)\)"
        parts = re.split(pattern, text)

        # re.split with groups produces: [text, alt1, url1, text, alt2, url2, text, ...]
        # Structure: i % 3 == 0 is text, i % 3 == 1 is alt, i % 3 == 2 is url
        for i in range(len(parts)):
            if i % 3 == 0:
                # Text part
                if parts[i]:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
            elif i % 3 == 1:
                # Image: alt text at i, url at i+1
                alt_text = parts[i]
                url = parts[i + 1]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
        parts = re.split(pattern, text)

        # re.split with groups produces: [text, link_text1, url1, text, link_text2, url2, text, ...]
        # Structure: i % 3 == 0 is text, i % 3 == 1 is link_text, i % 3 == 2 is url
        for i in range(len(parts)):
            if i % 3 == 0:
                # Text part
                if parts[i]:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
            elif i % 3 == 1:
                # Link: text at i, url at i+1
                link_text = parts[i]
                url = parts[i + 1]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
