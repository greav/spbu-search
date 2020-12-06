import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


class TextProcessor:
    def __init__(self, pattern="[A-Za-zА-Яа-я0-9_-]+"):
        self.pattern_re = re.compile(pattern)
        self.stemmer = SnowballStemmer("russian")

    def is_word(self, word):
        return bool(self.pattern_re.fullmatch(word))

    def process(self, text):
        for sent in sent_tokenize(text, language="russian"):
            for token in word_tokenize(sent, language="russian"):
                if self.is_word(token):
                    yield self.stemmer.stem(token.lower())
