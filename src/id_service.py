import csv
import os
from collections import defaultdict


class IDService:
    def __init__(self, index):
        self.index = index

    def create_word_ids(self):
        word_ids_file = os.path.join("data", "word_ids.csv")
        with open(word_ids_file, "w+", encoding="utf8", newline="") as f:
            csv_writer = csv.writer(f, delimiter=",")
            for id_, word in enumerate(self.index, start=1):
                csv_writer.writerow([id_, word])

    def create_post_ids(self):
        doc_freq = defaultdict(int)
        for word in self.index:
            for doc in self.index[word]:
                doc_freq[doc] += 1

        sorted_docs = sorted(doc_freq.items(), key=lambda item: item[1], reverse=True)
        print(f"Max df is: {sorted_docs[0][1]}")

        post_ids_file = os.path.join("data", "document_ids.csv")
        with open(post_ids_file, "w+", encoding="utf8", newline="") as f:
            csv_writer = csv.writer(f, delimiter=",")
            for id_, (doc, _) in enumerate(sorted_docs, start=1):
                csv_writer.writerow([id_, doc])

    @staticmethod
    def get_document_ids():
        document_ids = {}
        post_ids_file = os.path.join("data", "document_ids.csv")
        if not os.path.exists(post_ids_file):
            raise Exception("run create_post_ids() first")
        with open(post_ids_file, encoding="utf8") as f:
            csv_file = csv.reader(f)
            for id_, url in csv_file:
                document_ids[url] = id_
        return document_ids

    @staticmethod
    def get_word_ids():
        word_ids = {}
        word_ids_file = os.path.join("data", "word_ids.csv")
        if not os.path.exists(word_ids_file):
            raise Exception("run create_word_ids() first")
        with open(word_ids_file, encoding="utf8") as f:
            csv_file = csv.reader(f)
            for id_, word in csv_file:
                word_ids[word] = id_
        return word_ids
