import os

from src.id_service import IDService
from src.inverted_index import InvertedIndex


def main():
    collection_file = os.path.join("data", "news.csv")
    index_file = os.path.join("data", "inverted_index.pkl")

    if not os.path.exists(index_file):
        inverted_index = InvertedIndex()
        inverted_index.create_index(collection_file)
        inverted_index.save(index_file)

    inverted_index = InvertedIndex.load(index_file)

    id_service = IDService(inverted_index)
    id_service.create_post_ids()
    id_service.create_word_ids()


if __name__ == "__main__":
    main()
