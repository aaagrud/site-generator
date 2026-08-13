import unittest
from src.helpers.website_generation_helpers import extract_header

class TestExtractionHelpers(unittest.TestCase):
    def test_extract_header_h1_only(self):
        md: str = '''# Hello There
'''
        output: str =  extract_header(md)
        self.assertEqual(output, "Hello There")

    def test_extract_header_h1_with_p(self):
        md: str = '''# Hello There

How are you doing? I am good
'''
        output: str =  extract_header(md)
        self.assertEqual(output, "Hello There")

    def test_extract_header_h1_not_top(self):
        md: str = '''
How are you doing? I am good

# Hello There
'''
        output: str =  extract_header(md)
        self.assertEqual(output, "Hello There")

    def test_extract_header_h1_not_top(self):
        md: str = '''
How are you doing? I am good

Hello There
'''
        with self.assertRaises(Exception):
            extract_header(md)