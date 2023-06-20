from api.wordnet_api import WordNetApi
from api.word_2_vec_api import Word2VecApi
from api.kanji_db import KanjiDB
from model.relevant_phrase import RelevantPhrase
from typing import List


class RelevantPhraseFinder:
    def __init__(self):
        self.wordnet_api = WordNetApi()
        self.word2vec_api = Word2VecApi()
        self.kanji_db = KanjiDB()

    """
    takes an English word and outputs phrases that are related to it.
    uses multiple apis to make decisions
    """
    def findRelevantPhrases(self, base_word: str) -> List[RelevantPhrase]:
        relevant_phrases: List[RelevantPhrase] = []
        word2vec_relevant_phrases = self._find_relevant_phrases_by_word2vec(base_word)
        relevant_phrases.extend(word2vec_relevant_phrases)
        wordnet_relevant_phrases = self._find_relevant_phrases_by_wordnet(base_word)
        relevant_phrases.extend(wordnet_relevant_phrases)

        return relevant_phrases


    def _find_relevant_phrases_by_word2vec(self, base_word: str) -> List[RelevantPhrase]:
        word2vec_similar_words = self.word2vec_api.find_similar_words(base_word)
        relevant_phrases = []
        for sw in word2vec_similar_words:
            translations = self.wordnet_api.translate(sw)
            for t in translations:
                relevant_phrases.append(t.phrase)

        return relevant_phrases

    def _find_relevant_phrases_by_wordnet(self, base_word: str) -> List[str]:
        relevant_phrases = []
        translations = self.wordnet_api.translate(base_word)
        for t in translations:
            relevant_phrases.append(t.phrase)

        unique_synsets = set()
        for t in translations:
            unique_synsets.add(t.synset)
        for synset in unique_synsets:
            similar_words = self.wordnet_api.find_similar_words(synset)
            relevant_phrases.extend([w.phrase for w in similar_words])

        return relevant_phrases