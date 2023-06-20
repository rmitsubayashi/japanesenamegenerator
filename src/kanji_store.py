from model.kanji import Kanji
from typing import List
from util.language_utils import LanguageUtils


"""
stores Kanji in a temporary storage that will be O(1) access.
This is for reduced runtime of the KanjiNameFitter algorithm.
This is stored in a trie because tries are cool.
Nothing wrong with just making a map of every pronunciation and associated Kanjis :)
"""
class KanjiStore:

    def __init__(self):
        self._resetStore()

    def _resetStore(self):
        self.headNode = self.TrieNode("")

    def find_best_match(self, phonemes: List[str]) -> List[Kanji]:
        currentNode = self.headNode
        for p in phonemes:
            if not currentNode.leafExists(p):
                return None
            currentNode = currentNode.find(p)
        if currentNode.kanjis:
            return self._select_best_weight_kanjis(currentNode.kanjis)
        else:
            # eg store has "いん" and we are finding "い". 
            # "い" will exist but will not have any kanji stored in the node.
            return None
        
    # assumes input list is in weight order
    def _select_best_weight_kanjis(self, kanjis: List[Kanji]) -> List[Kanji]:
        max = -1
        output_list = []
        for k in kanjis:
            if k.similarity_score >= max:
                output_list.append(k)
                max = k.similarity_score
            else:
                break
        return output_list

    def storeKanjis(self, weighted_kanjis: List[Kanji]):
        sorted_kanjis = sorted(weighted_kanjis, key = lambda kanji: kanji.similarity_score, reverse=True)
        for k in sorted_kanjis:
            self._storeKanji(k)

    def _storeKanji(self, weighted_kanji: Kanji):
        if weighted_kanji.similarity_score == None:
            raise Exception("no weight on this kanji: " + weighted_kanji.kanji)

        # there will be at most 2 pronunciations.
        # one for just main (ie 帰る -> かえ)
        # and one for main + okurigana (ie 帰る -> かえる).
        # note that different pronunciations for the same kanji (ie 帰る、帰宅)
        # will be stored in separate objects
        pronunciation = weighted_kanji.pronunciation.main
        pronunciation_phonemes = LanguageUtils().splitHiraganaIntoPhonemes(pronunciation)
        self._recurseAndAddTrieNode(self.headNode, pronunciation_phonemes, weighted_kanji)

        if weighted_kanji.pronunciation.okurigana != "":
            pronunciation_plus_okurigana = pronunciation + weighted_kanji.pronunciation.okurigana
            pronunciation_plus_okurigana_phonemes = LanguageUtils().splitHiraganaIntoPhonemes(pronunciation_plus_okurigana)
            self._recurseAndAddTrieNode(self.headNode, pronunciation_plus_okurigana_phonemes, weighted_kanji)

    class TrieNode:
        def __init__(self, phoneme: str):
            self.phoneme = phoneme
            self.kanjis = []
            self.leaves = []

        def addKanji(self, kanji: Kanji):
            # kanjis are added in weight order, so the trie node will also in weight order
            self.kanjis.append(kanji)
        
        def addLeaf(self, leaf):
            self.leaves.append(leaf)

        def leafExists(self, phoneme: str) -> bool:
            for leaf in self.leaves:
                if leaf.phoneme == phoneme:
                    return True
            return False

        def find(self, phoneme: str):
            for leaf in self.leaves:
                if leaf.phoneme == phoneme:
                    return leaf
            return None


    def _recurseAndAddTrieNode(self, node: TrieNode, remainingPhonemes: List[str], kanji: Kanji):
        nextLeaf = self._findOrAddLeaf(node, remainingPhonemes[0])
        if len(remainingPhonemes) == 1:
            nextLeaf.addKanji(kanji)
            return
        
        self._recurseAndAddTrieNode(nextLeaf, remainingPhonemes[1:], kanji)


    def _findOrAddLeaf(self, node: TrieNode, phoneme: str) -> TrieNode:
        if node.leafExists(phoneme):
            return node.find(phoneme)
        else:
            newLeaf = self.TrieNode(phoneme)
            node.addLeaf(newLeaf)
            return newLeaf