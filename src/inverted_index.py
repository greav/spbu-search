import os
import pickle
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

from .encoding import (
    elias_delta_decode,
    elias_delta_encode_sequence,
    elias_gamma_decode,
    elias_gamma_encode_sequence,
)
from .id_service import IDService
from .preprocessor import TextProcessor

COMPRESSION_ENCODING = {
    "elias_gamma": elias_gamma_encode_sequence,
    "elias_delta": elias_delta_encode_sequence,
}
COMPRESSION_DECODING = {
    "elias_gamma": elias_gamma_decode,
    "elias_delta": elias_delta_decode,
}


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.text_processor = TextProcessor()
        self.id_service = IDService()
        self.compress_method = None

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

        self.index = defaultdict(list)
        for _, row in tqdm(collection.iterrows()):
            words = self.text_processor.process(row["text"])
            for word in words:
                self.index[word].append(row["id"])

        self.id_service.create_post_ids(self.index)

        for word in self.index:
            self.index[word] = [
                self.id_service.doc_to_id[doc] for doc in self.index[word]
            ]

    def compress(self, compress_method="elias_delta"):
        if self.compress_method:
            raise Exception(
                f"Index already compressed by {self.compress_method} method"
            )
        if compress_method in COMPRESSION_ENCODING:
            self.compress_method = compress_method
            for word in self.index:
                self.index[word] = COMPRESSION_ENCODING[compress_method](
                    self.index[word]
                )
        else:
            raise Exception("Invalid prameter for compress_method")

    def save(self, file_path):
        if os.path.exists(file_path):
            raise Exception("Index already exists")

        if not self.index:
            raise Exception("You should create index before saving")

        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_path):
        if not os.path.exists(file_path):
            raise Exception("File doesn't exist")

        with open(file_path, "rb") as f:
            index = pickle.load(f)
        return index

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def __getitem__(self, key):
        if key not in self.index:
            raise KeyError(f"{key} doesn't belong to index")

        if self.compress_method is None:
            return [self.id_service.id_to_doc[id_] for id_ in self.index[key]]
        else:
            return [
                self.id_service.id_to_doc[id_]
                for id_ in COMPRESSION_DECODING[self.compress_method](self.index[key])
            ]

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return []
