import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Test capturing multiple images correctly"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_single(self):
        """Test capturing a single isolated image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        """Test capturing multiple links correctly"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(matches, expected)

    def test_extract_links_should_ignore_images(self):
        """Ensure link extraction does not mistakenly match image syntax"""
        text = "Check out this [website](https://google.com) and look at this image: ![cat](https://cats.com/pic.jpg)"
        matches = extract_markdown_links(text)
        expected = [("website", "https://google.com")]
        self.assertEqual(matches, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "Text with ![alt](https://example.com/image.jpg) in middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/image.jpg"),
                TextNode(" in middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/pic.png) at start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
                TextNode(" at start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "End with image ![pic](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("End with image ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![only](https://example.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.IMAGE, "https://example.com/only.png"),
            ],
            new_nodes,
        )

    def test_split_image_multiple_consecutive(self):
        node = TextNode(
            "Multiple: ![first](url1) ![second](url2) ![third](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Multiple: ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "url2"),
                TextNode(" ", TextType.TEXT),
                TextNode("third", TextType.IMAGE, "url3"),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode("This has no images at all", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_preserves_non_text_nodes(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(
                "Text with ![image](https://example.com/pic.png)",
                TextType.TEXT,
            ),
            TextNode("italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_image_complex_urls(self):
        node = TextNode(
            "Image ![alt text](https://example.com/path/to/image.png?param=value&other=123) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image ", TextType.TEXT),
                TextNode(
                    "alt text",
                    TextType.IMAGE,
                    "https://example.com/path/to/image.png?param=value&other=123",
                ),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "Check [this](https://example.com) out",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("this", TextType.LINK, "https://example.com"),
                TextNode(" out", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://example.com) at start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "End with [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("End with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode(
            "[only](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_link_multiple_consecutive(self):
        node = TextNode(
            "Visit [first](url1) [second](url2) [third](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("first", TextType.LINK, "url1"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.LINK, "url2"),
                TextNode(" ", TextType.TEXT),
                TextNode("third", TextType.LINK, "url3"),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode("This has no links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_preserves_non_text_nodes(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(
                "Text with [link](https://example.com)",
                TextType.TEXT,
            ),
            TextNode("italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_link_ignores_images(self):
        """Links should not match image syntax"""
        node = TextNode(
            "Check [link](https://google.com) and ![image](https://example.com/pic.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and ![image](https://example.com/pic.jpg)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_complex_urls(self):
        node = TextNode(
            "See [documentation](https://example.com/docs?page=1&lang=en#section)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode(
                    "documentation",
                    TextType.LINK,
                    "https://example.com/docs?page=1&lang=en#section",
                ),
            ],
            new_nodes,
        )

    def test_split_link_complex_text(self):
        node = TextNode(
            "Link text can have [special chars !@#$%](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link text can have ", TextType.TEXT),
                TextNode("special chars !@#$%", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        """Test the example from the requirements"""
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        nodes = text_to_textnodes(text)
        expected = [
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
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        """Plain text with no formatting"""
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just plain text", TextType.TEXT)], nodes)

    def test_text_to_textnodes_bold_only(self):
        """Text with only bold"""
        text = "This is **bold**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic_only(self):
        """Text with only italic"""
        text = "This is _italic_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_text_to_textnodes_code_only(self):
        """Text with only code"""
        text = "Use `variable` here"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("variable", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_image_only(self):
        """Text with only image"""
        text = "![alt](https://example.com/pic.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/pic.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_link_only(self):
        """Text with only link"""
        text = "[click here](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("click here", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_bold(self):
        """Text with multiple bold segments"""
        text = "**first** and **second**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_types(self):
        """Multiple formatting types in sequence"""
        text = "**bold** then _italic_ then `code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_nested_visually(self):
        """Text with multiple formatting types mixed"""
        text = "**bold _and italic_** plus `code`"
        nodes = text_to_textnodes(text)
        # The parser processes bold first, extracting "bold _and italic_" as bold
        # Then italic processing can't split inside bold nodes (non-TEXT)
        self.assertListEqual(
            [
                TextNode("bold _and italic_", TextType.BOLD),
                TextNode(" plus ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_image_and_link(self):
        """Text with both images and links"""
        text = "See ![pic](url1) and [link](url2)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url2"),
            ],
            nodes,
        )

    def test_text_to_textnodes_all_types(self):
        """Text combining all formatting types"""
        text = "**bold** _italic_ `code` ![image](https://i.imgur.com/img.png) [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/img.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_adjacent_formatting(self):
        """Adjacent formatting without spaces"""
        text = "**bold**_italic_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        """Empty string input"""
        text = ""
        nodes = text_to_textnodes(text)
        # Empty strings get filtered out by split_nodes_delimiter
        self.assertListEqual([], nodes)

    def test_text_to_textnodes_complex_scenario(self):
        """Complex real-world-like text"""
        text = "Check out the **official documentation** for _more_ `details` or see ![screenshot](screen.png) and [link](https://docs.example.com)"
        nodes = text_to_textnodes(text)
        # Links inside bold text won't be parsed (bold nodes aren't TEXT type)
        self.assertListEqual(
            [
                TextNode("Check out the ", TextType.TEXT),
                TextNode("official documentation", TextType.BOLD),
                TextNode(" for ", TextType.TEXT),
                TextNode("more", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("details", TextType.CODE),
                TextNode(" or see ", TextType.TEXT),
                TextNode("screenshot", TextType.IMAGE, "screen.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://docs.example.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes_special_chars_in_url(self):
        """URLs with query params and fragments"""
        text = "Visit [docs](https://example.com/page?id=123&lang=en#section)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://example.com/page?id=123&lang=en#section"),
            ],
            nodes,
        )

    def test_text_to_textnodes_repeated_formatting(self):
        """Same formatting applied multiple times"""
        text = "**one** **two** **three**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
