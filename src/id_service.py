from collections import defaultdict


class IDService:
    def __init__(self):
        self.id_to_doc = {}
        self.doc_to_id = {}

    def create_post_ids(self, index):
        doc_freq = defaultdict(int)
        for word in index:
            for doc in index[word]:
                doc_freq[doc] += 1

        sorted_docs = sorted(doc_freq.items(), key=lambda item: item[1], reverse=True)
        print(f"Max document frequency is: {sorted_docs[0][1]}")

        for id_, (doc, _) in enumerate(sorted_docs, start=1):
            self.id_to_doc[id_] = doc
            self.doc_to_id[doc] = id_
