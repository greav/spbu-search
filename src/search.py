from collections import Counter

import pandas as pd

from .inverted_index import InvertedIndex
from .preprocessor import TextProcessor


class SearchClient:
    def __init__(self, index_path, collection_path, top_n=10):
        self.index = InvertedIndex.load(index_path)
        self.collection = self.load_collection(collection_path)
        self.text_processor = TextProcessor()
        self.top_n = top_n

    @staticmethod
    def load_collection(path):
        collection = pd.read_csv(
            path,
            names=[
                "id",
                "author",
                "likes_count",
                "views_count",
                "comments_count",
                "reports_count",
                "publication_date",
                "text",
                "type",
            ],
        )
        return {row["id"]: row for row in collection.to_dict(orient="records")}

    def search(self, query):
        relevant_docs = []
        for token in self.text_processor.process(query):
            relevant_docs += self.index.get(token)
        most_common = Counter(relevant_docs).most_common(n=self.top_n)
        return [self.collection[id_] for id_, _freq in most_common]
