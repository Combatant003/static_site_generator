import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """Test a simple paragraph tag rendering"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        """Test an anchor tag rendering with properties"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_raw_text(self):
        """Test rendering when tag is None (should return raw text)"""
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_no_value_raises_error(self):
        """Test that a ValueError is raised if value is missing"""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        """Verify the string representation doesn't contain a children field"""
        node = LeafNode("span", "text", {"class": "bold"})
        self.assertEqual(
            repr(node), "LeafNode(tag='span', value='text', props={'class': 'bold'})"
        )


if __name__ == "__main__":
    unittest.main()
