import unittest
from unittest.mock import Mock
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from api.kanji_db import KanjiDB
from model.kanji import Kanji
from model.kanji import Pronunciation
from model.relevant_phrase import RelevantPhrase
from weighted_kanji_generator import WeightedKanjiGenerator

class WeightedKanjiGeneratorTest(unittest.TestCase):
    def test_weight(self):
        kanji_db = KanjiDB()
        relevant_phrase_finder = Mock()
        relevant_phrase_finder.findRelevantPhrases.return_value = [RelevantPhrase("木", "tree")]

        weighted_kanji_generator = WeightedKanjiGenerator(relevant_phrase_finder, kanji_db)
        result = weighted_kanji_generator.generate_weighted_kanji([""])

        self.assertEqual(1, result.find_best_match("き")[0].similarity_score)
        self.assertEqual(0, result.find_best_match("きん")[0].similarity_score)

    def test_relevant_kanji(self):
        kanji_db = KanjiDB()
        relevant_phrase_finder = Mock()
        relevant_phrase = RelevantPhrase("木", "tree")
        relevant_phrase_finder.findRelevantPhrases.return_value = [relevant_phrase]

        weighted_kanji_generator = WeightedKanjiGenerator(relevant_phrase_finder, kanji_db)
        result = weighted_kanji_generator.generate_weighted_kanji([""])

        self.assertEqual(relevant_phrase.japanese, result.find_best_match("き")[0].relevant_phrases[0].japanese)
        self.assertEqual(0, len(result.find_best_match("きん")[0].relevant_phrases))
