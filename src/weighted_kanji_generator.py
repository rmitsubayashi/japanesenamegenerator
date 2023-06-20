from relevant_phrase_finder import RelevantPhraseFinder
from kanji_store import KanjiStore
from api.kanji_db import KanjiDB
from model.relevant_phrase import RelevantPhrase
from util.language_utils import LanguageUtils
from typing import List
import copy

class WeightedKanjiGenerator:
    def __init__(self, relevant_phrase_finder: RelevantPhraseFinder, kanjiDB: KanjiDB):
        self.relevant_phrase_finder = relevant_phrase_finder
        self.kanji_db = kanjiDB

    """
    takes the user's input (words that describe the user in ENGLISH) and generates a Kanji Store
    with weights on kanji that relate to the user's input.
    For now, weights will be 1 or 0 (1 if similar, 0 if not). can update as needed.
    """
    def generate_weighted_kanji(self, user_properties: List[str]) -> KanjiStore:
        relevant_phrases_by_kanji_str = dict()
        for p in user_properties:
            # simliar kanji 
            relevant_phrases = self.relevant_phrase_finder.findRelevantPhrases(p)
            language_utils = LanguageUtils()
            for word in relevant_phrases:
                extracted_kanjis = language_utils.extractKanjis(word.japanese)
                for k in extracted_kanjis:
                    if k in relevant_phrases_by_kanji_str.keys():
                        k_relevant_phrases: List[RelevantPhrase] = relevant_phrases_by_kanji_str[k]
                        k_relevant_phrases.append(word)
                    else:
                        k_relevant_phrases = [word]
                        relevant_phrases_by_kanji_str[k] = k_relevant_phrases

        weighted_kanjis = []
        for key, value in self.kanji_db.kanji_lookup_table.items():
            weight = 0
            relevant_phrases = []
            if key in relevant_phrases_by_kanji_str:
                weight = 1
                relevant_phrases.extend(relevant_phrases_by_kanji_str[key])
            for v in value:
                k = copy.deepcopy(v)
                k.similarity_score = weight
                k.relevant_phrases = relevant_phrases
                weighted_kanjis.append(k)
        store = KanjiStore()
        store.storeKanjis(weighted_kanjis)

        return store
        