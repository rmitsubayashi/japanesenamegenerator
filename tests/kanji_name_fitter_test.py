import unittest
from unittest.mock import Mock

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from kanji_store import KanjiStore
from kanji_name_fitter import KanjiNameFitter
from tests.util.test_utils import TestUtils

class KanjiNameFitterTest(unittest.TestCase):
    def setUp(self):
        self.testUtils = TestUtils(self)

    def test_input_order(self):
        combination_generator = Mock()
        combination_generator.createCombinations.return_value = [['い','ん']]
        kanji_store = KanjiStore()
        expected = self.testUtils.createWeightedKanji("院", "いん", "", 0.6)
        kanji_store.storeKanjis([expected, self.testUtils.createWeightedKanji("員", "いん", "", 0.1)])
        kanji_name_fitter = KanjiNameFitter(combination_generator, kanji_store)

        result = kanji_name_fitter.fit("")
        self.assertEqual([expected], result)

        # test different order
        kanji_store = KanjiStore()
        expected = self.testUtils.createWeightedKanji("員", "いん", "", 0.6)
        kanji_store.storeKanjis([self.testUtils.createWeightedKanji("院", "いん", "", 0.1), expected])
        kanji_name_fitter = KanjiNameFitter(combination_generator, kanji_store)

        result = kanji_name_fitter.fit("")
        self.assertEqual([expected], result)

    def test_multiple_kanjis(self):
        combination_generator = Mock()
        combination_generator.createCombinations.return_value = [['し','た']]
        kanji_store = KanjiStore()
        shi = self.testUtils.createWeightedKanji("死", "し", "", 0.6)
        ta = self.testUtils.createWeightedKanji("田", "た", "", 0.1)
        shita = self.testUtils.createWeightedKanji("下", "した", "", 0.2)
        kanji_store.storeKanjis([shi, ta, shita])
        kanji_name_fitter = KanjiNameFitter(combination_generator, kanji_store)

        result = kanji_name_fitter.fit("")
        self.assertEqual([shi, ta], result)

    def test_multiple_pronnunciations(self):
        combination_generator = Mock()
        combination_generator.createCombinations.return_value = [['す','う'],['す']]
        kanji_store = KanjiStore()
        su = self.testUtils.createWeightedKanji("酢", "す","", 0.6)
        suu = self.testUtils.createWeightedKanji("数", "すう", "", 0.1)
        kanji_store.storeKanjis([su, suu])
        kanji_name_fitter = KanjiNameFitter(combination_generator, kanji_store)

        result = kanji_name_fitter.fit("")
        self.assertEqual([su], result)
        