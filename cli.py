import os

from src.inverted_index import InvertedIndex


def main():
    collection_file = os.path.join("data", "news.csv")
    index_file = os.path.join("data", "inverted_index.pkl")
    index_gamma_file = os.path.join("data", "inverted_index_gamma_compressed.pkl")
    index_delta_file = os.path.join("data", "inverted_index_delta_compressed.pkl")

    if not os.path.exists(index_file):
        inverted_index = InvertedIndex()
        inverted_index.create_index(collection_file)
        inverted_index.save(index_file)

    if not os.path.exists(index_gamma_file):
        inverted_index = InvertedIndex.load(index_file)
        inverted_index.compress(compress_method="elias_gamma")
        inverted_index.save(index_gamma_file)

    if not os.path.exists(index_delta_file):
        inverted_index = InvertedIndex.load(index_file)
        inverted_index.compress(compress_method="elias_delta")
        inverted_index.save(index_delta_file)


if __name__ == "__main__":
    main()
