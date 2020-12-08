import os
import unittest
from src.inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.invertedIndex = InvertedIndex()

    # Test for compress()
    def test_compress(self):
        self.assertRaises(Exception, self.invertedIndex.compress, "elias")
        print("#1: OK")

    # Tests for save()

    # Test for Exception("You should create index before saving")
    def test_save_without_creating(self):
        index_file = os.path.join("test_data", "inverted_index.pkl")
        self.assertRaises(Exception, self.invertedIndex.save, index_file)
        print("#2: OK")

    # Test for Exception("Index already exists")
    def test_save_for_existing(self):
        collection_file = os.path.join("test_data", "news.csv")
        index_file = os.path.join("test_data", "inverted_index.pkl")
        self.invertedIndex.create_index(collection_file)
        self.assertRaises(Exception, self.invertedIndex.save, index_file)
        print("#3: OK")


if __name__ == "__main__":
    unittest.main()