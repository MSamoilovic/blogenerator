import unittest

from markdown.converter import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_h1_among_other_content(self):
        md = "Some text\n# My Title\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_h2_is_not_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Not an h1")

    def test_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a plain paragraph.")

    def test_picks_first_h1(self):
        md = "# First\n# Second"
        self.assertEqual(extract_title(md), "First")


if __name__ == "__main__":
    unittest.main()
