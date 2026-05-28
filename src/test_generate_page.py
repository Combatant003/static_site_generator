import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_multiline(self):
        md = "Some text\n\n# My Title\n\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not h1\n\nsome text")

    def test_ignores_h2(self):
        with self.assertRaises(ValueError):
            extract_title("## Heading 2")

    def test_first_h1_wins(self):
        md = "# First\n# Second"
        self.assertEqual(extract_title(md), "First")


if __name__ == "__main__":
    unittest.main()
