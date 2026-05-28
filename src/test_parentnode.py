import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        """Test a parent node with a single leaf child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test deep recursion by nesting a ParentNode inside a ParentNode"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_mixed_children(self):
        """Test the assignment example with mixed LeafNodes (with and without tags)"""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        """Test that a ParentNode correctly renders its own HTML attributes"""
        child = LeafNode("span", "hello")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>hello</span></div>',
        )

    def test_missing_tag_raises_error(self):
        """Test that a missing tag correctly throws a ValueError"""
        child = LeafNode("p", "text")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("must have a tag", str(context.exception))

    def test_empty_children_raises_error(self):
        """Test that missing or empty children list throws a ValueError"""
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("must have children", str(context.exception))


if __name__ == "__main__":
    unittest.main()
