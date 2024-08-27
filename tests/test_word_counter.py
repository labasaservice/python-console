# tests/test_word_counter.py
import unittest
from src.word_counter import count_characters

class TestWordCounter(unittest.TestCase):
    def test_count_characters(self):
        self.assertEqual(count_characters("hello"), 5)
        self.assertEqual(count_characters(""), 0)
        self.assertEqual(count_characters("python"), 6)

if __name__ == "__main__":
    unittest.main()