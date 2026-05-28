import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty_blocks_removed(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Section"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Deep"), BlockType.HEADING)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

    def test_code_no_newline(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_quote_single(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> quote text"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line1\n> line2"), BlockType.QUOTE)

    def test_quote_missing_gt(self):
        self.assertEqual(block_to_block_type("> line1\nline2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item1\n- item2"), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH)

    def test_ordered_list_gap(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """# H1 heading

## H2 with **bold**

### H3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1 heading</h1><h2>H2 with <b>bold</b></h2><h3>H3</h3></div>",
        )

    def test_quote(self):
        md = """> This is a quote
> with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- item one
- item **two**
- item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. first
2. second with `code`
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <code>code</code></li><li>third</li></ol></div>",
        )
