import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        """Test formatting multiple attributes with leading spaces"""
        node = HTMLNode(
            tag="a",
            value="Click here",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        """Test that an empty or missing props dict returns an empty string"""
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        """Test formatting a single attribute"""
        node = HTMLNode(tag="img", props={"src": "cat.jpg"})
        self.assertEqual(node.props_to_html(), ' src="cat.jpg"')

    def test_repr_output(self):
        """Verify the string representation includes all properties properly"""
        node = HTMLNode(tag="h1", value="Title")
        expected_repr = "HTMLNode(tag='h1', value='Title', children=[], props={})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
