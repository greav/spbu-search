import unittest
from src.preprocessor import TextProcessor


class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        self.textProcessor = TextProcessor()

    # True tests for is_word()

    # 1
    def test_is_word_true_for_rus(self):
        self.assertEqual(self.textProcessor.is_word("ректор"), True)

    # 2
    def test_is_word_true_for_eng(self):
        self.assertEqual(self.textProcessor.is_word("rector"), True)

    # 3
    def test_is_word_true_for_numbers(self):
        self.assertEqual(self.textProcessor.is_word("35614"), True)

    # 4
    def test_is_word_true_for_letters_and_numbers(self):
        self.assertEqual(self.textProcessor.is_word("re35ll6"), True)

    # 5
    def test_is_word_true_for_numbers_and_letters(self):
        self.assertEqual(self.textProcessor.is_word("35as6kmlk"), True)

    # False tests for is_word()

    # 6
    def test_is_word_false_for_special_character_first(self):
        self.assertEqual(self.textProcessor.is_word(":rector"), False)

    # 7
    def test_is_word_false_for_special_character_middle(self):
        self.assertEqual(self.textProcessor.is_word("rec,tor"), False)

    # 8
    def test_is_word_false_for_special_character_last(self):
        self.assertEqual(self.textProcessor.is_word("rector."), False)

    # Tests for process()

    # 9
    def test_process_rus(self):
        self.assertEqual(list(self.textProcessor.process("Мама мыла раму.")), ['мам', 'мыл', 'рам'])

    # 10
    def test_process_eng(self):
        self.assertEqual(list(self.textProcessor.process("Cats love to walk.")), ['cats', 'love', 'to', 'walk'])


if __name__ == "__main__":
    unittest.main()
