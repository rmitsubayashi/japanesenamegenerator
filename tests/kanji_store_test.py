import unittest

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from kanji_store import KanjiStore
from tests.util.test_utils import TestUtils

class KanjiStoreTest(unittest.TestCase):
    def setUp(self):
        self.testUtils = TestUtils(self)

    def test_store_access(self):
        expected = self.testUtils.createWeightedKanji("君", "きみ", "", 1)
        input = [expected]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("きみ")
        self.assertEqual(expected, result[0])

    def test_part(self):
        whole = self.testUtils.createWeightedKanji("君", "きみ", "", 1)
        input = [whole]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("き")
        self.assertEqual(None, result)

    def test_different_weight(self):
        expected = self.testUtils.createWeightedKanji("君", "きみ", "", 1)
        less_weight = self.testUtils.createWeightedKanji("君", "きみ", "", 0)
        input = [less_weight, expected]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("きみ")
        self.assertEqual(expected, result[0])

        input_reordered = [expected, less_weight]
        store = KanjiStore()
        store.storeKanjis(input_reordered)
        result = store.find_best_match("きみ")
        self.assertEqual(expected, result[0])

    def test_same_first_letter(self):
        expected = self.testUtils.createWeightedKanji("君", "きみ", "", 1)
        expected_same_first_letter = self.testUtils.createWeightedKanji("菊", "きく", "", 1)
        input = [expected, expected_same_first_letter]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("きみ")
        self.assertEqual(expected, result[0])
        result_same_first_letter = store.find_best_match("きく")
        self.assertEqual(expected_same_first_letter, result_same_first_letter[0])

    def test_included(self):
        expected = self.testUtils.createWeightedKanji("君", "きみ", "", 1)
        expected_included = self.testUtils.createWeightedKanji("木", "き", "", 1)
        input = [expected, expected_included]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("きみ")
        self.assertEqual(expected, result[0])
        result_included = store.find_best_match("き")
        self.assertEqual(expected_included, result_included[0])

    def test_okurigana(self):
        expected = self.testUtils.createWeightedKanji("聞く", "き", "く", 1)
        input = [expected]
        store = KanjiStore()
        store.storeKanjis(input)
        result = store.find_best_match("き")
        self.assertEqual(expected, result[0])
        result_okurigana = store.find_best_match("きく")
        self.assertEqual(expected, result_okurigana[0])

