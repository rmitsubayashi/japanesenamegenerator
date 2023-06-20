import io
import unittest
from typing import List

from model.kanji import Kanji
from model.kanji import Pronunciation

class TestUtils:
    def __init__(self, test: unittest.TestCase):
        self.test = test

    def assertListContentEqualIgnoringOrder(self, expected: List[object], toCompare: List[object]):
        toCompareCopy = toCompare.copy()
        for e in expected:
            self.test.assertIn(e, toCompare)
            toCompareCopy.remove(e)
        self.test.assertFalse(toCompareCopy)

    def getNames(self) -> List[str]:
        lines: List[str] = []
        with io.open('data/foreign_names.txt', mode='r', encoding='utf-8') as file:
            fileLines = file.readlines()
            for line in fileLines:
                lines.append(line.strip())
            file.close()
        return lines
    
    def createWeightedKanji(self, kanji: str, main_pronunciation: str, okurigana: str, weight: int) -> Kanji:
        k = Kanji(kanji, Pronunciation(main_pronunciation, okurigana))
        k.similarity_score = weight
        return k