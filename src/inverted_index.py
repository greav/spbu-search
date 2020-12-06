import os
import pickle
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

from .preprocessor import TextProcessor


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.text_processor = TextProcessor()

    def create_index(self, collection_path):
        collection = pd.read_csv(
            collection_path,
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
        collection = collection[~collection["text"].isna()]

        for _, row in tqdm(collection.iterrows()):
            words = self.text_processor.process(row["text"])
            for word in words:
                self.index[word].append(row["id"])

    def save(self, file_path):
        if os.path.exists(file_path):
            raise Exception("Index already exists")

        if not self.index:
            raise Exception("You should create index before saving")

        with open(file_path, "wb") as f:
            pickle.dump(self.index, f)

    @classmethod
    def load(cls, file_path):
        if not os.path.exists(file_path):
            raise Exception("File doesn't exist")

        with open(file_path, "rb") as f:
            index = pickle.load(f)
        instance = cls()
        instance.index = index
        return instance

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def __getitem__(self, key):
        if key not in self.index:
            raise KeyError(f"{key} doesn't belong to index")
        return self.index[key]

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return []
