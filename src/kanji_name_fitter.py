from model.kanji import Kanji
from pronunciation_combination_generator import PronunciationCombinationGenerator
from kanji_store import KanjiStore
from typing import List
import random
import copy
Phoneme = str

class KanjiNameFitter:

    def __init__(
        self, 
        pronunciationCombinationGenerator: PronunciationCombinationGenerator,
        kanjiStore: KanjiStore
    ):
        self.combinationGenerator = pronunciationCombinationGenerator
        self.kanjiStore = kanjiStore

    def fit(self, name: str) -> List[Kanji]:
        combinations = self.combinationGenerator.createCombinations(name)
        
        all_possible_kanjis = []
        for c in combinations:
            all_possible_kanjis.extend(self._fit_kanjis(c))

        for ks in all_possible_kanjis:
            k_str = ""
            for k in ks:
                k_str += k.kanji
            print(k_str)
        
        best_kanjis = []
        best_weight = -1

        for kanjis in all_possible_kanjis:
            avg = self._calculate_weight_average(kanjis)
            should_update = False
            if avg  > best_weight:
                should_update = True
            elif avg == best_weight:
                if len(kanjis) < len(best_kanjis[0]):
                    should_update = True
                elif len(kanjis) == len(best_kanjis[0]):
                    best_kanjis.append(kanjis)

            if should_update:
                best_kanjis = [kanjis]
                best_weight = avg

        return random.choice(best_kanjis)

    def _fit_kanjis(self, phonemes: List[Phoneme]) -> List[List[Kanji]]:
        result_arr = []
        self._recursively_find_kanji_paths(phonemes, [], [], result_arr)

        return result_arr

    """
    traverses each letter one by one. 
    each letter has two branches(leafs): 1 for when there is a kanji for that letter (including previous letters that don't have a kanji representation) 
    and 1 to skip the letter and go to the next letter (the next letter will include the previously skipped letter(s) to find a kanji representation).
    we do this to cover all possible kanji combinations for the letters.
    """
    def _recursively_find_kanji_paths(self, remainingPhonemes: List[Phoneme], skippedPhonemes: List[Phoneme], current_kanjis: List[Kanji], result_arr: List[List[Kanji]]):
        kanji_combinations = []
        
        toFind = skippedPhonemes.copy()
        toFind.append(remainingPhonemes[0])
        matchingKanjis = self.kanjiStore.find_best_match(toFind)

        new_kanjis = current_kanjis.copy()
        if matchingKanjis:
            new_kanji = copy.deepcopy(random.choice(matchingKanjis))
            new_kanji.selected_pronunciation = ''.join(toFind)
            new_kanjis.append(new_kanji)

        if len(remainingPhonemes) == 1:
            if matchingKanjis:
                result_arr.append(new_kanjis)
            return

        if matchingKanjis:
            kanji_combinations.append(self._recursively_find_kanji_paths(remainingPhonemes[1:], [], new_kanjis, result_arr))

        kanji_combinations.append(self._recursively_find_kanji_paths(remainingPhonemes[1:], toFind, current_kanjis.copy(), result_arr))

    def _calculate_weight_average(self, kanjis: List[Kanji]) -> float:
        character_count = 0
        total_weight = 0
        for k in kanjis:
            c = len(k.selected_pronunciation)
            character_count += c
            total_weight += c * k.similarity_score
        return total_weight / character_count