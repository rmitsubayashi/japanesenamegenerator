import io
from typing import List
import copy

# import sys
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '../..')))
# from src.model.kanji import Kanji
from model.kanji import Kanji

class KanjiDB:
    def __init__(self):
        self._loadKanjis()

    def _loadKanjis(self):
        with io.open('data/kanji_pronunciations.txt', mode='r', encoding='utf-8') as file:
            kanji_lookup_table = dict()
            for kanji_json in file:
                kanji = Kanji.from_string(kanji_json)
                if kanji.kanji not in kanji_lookup_table:
                    kanji_lookup_table[kanji.kanji] = []
                kanji_lookup_table[kanji.kanji].append(kanji)
            self.kanji_lookup_table = kanji_lookup_table
            file.close()

    """
    Description: takes a kanji string and returns an object with pronunciation

    Parameters:
        kanji: the kanji as a string character

    Return value:
        a list of Kanji objects. Each object contains a unique pronunciation of the same Kanji
    """
    def identifyKanji(self, kanji: str) -> List[Kanji]:
        if kanji in self.kanji_lookup_table:
            matching_kanji = self.kanji_lookup_table[kanji]
            return [ copy.deepcopy(k) for k in matching_kanji ]
        return []