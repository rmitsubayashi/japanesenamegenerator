from typing import Callable
from typing import List
from typing import Set
from util.language_utils import LanguageUtils

from util.list_utils import ListUtils

class PronunciationCombinationGenerator:
    def __init__(self, single_phoneme_rules: List[Callable[[str],str]], combination_phoneme_rules: List[Callable[[str,str],str]]):
        self.single_phoneme_rules = single_phoneme_rules
        self.combination_phoneme_rules = combination_phoneme_rules

    # returns a list of phonemes (we don't want "じゅ" to be parsed as "じ""ゅ")
    def createCombinations(self, hiragana: str) -> List[List[str]]:
        combination_phoneme_rule_combinations = self._createCombinationsUsingCombinationPhonemeRules(LanguageUtils().splitHiraganaIntoPhonemes(hiragana))
        combinations: List[List[str]] = []
        for combination in combination_phoneme_rule_combinations:
            combinations += self._createCombinationsUsingSinglePhonemeRules(combination)

        return combinations


    def _createCombinationsUsingSinglePhonemeRules(self, phonemes: List[str]) -> List[List[str]]:
        # string instead of list of characters so we can remove duplicates
        combinations: Set[str] = {''.join(phonemes)}
        characters_to_change: List[(int, List[str])] = []
        for index, c in enumerate(phonemes):
            for rule in self.single_phoneme_rules:
                alternate_phonemes = rule(c)
                if alternate_phonemes is not None:
                    characters_to_change.append((index, alternate_phonemes))

        characters_to_change_combinations = ListUtils().powerset(characters_to_change)
        for combination in characters_to_change_combinations:
            copy = phonemes.copy()
            # iterate in reverse order so we can change the characters without affecting index
            for index, alternate_phonemes in reversed(combination):
                copy[index:index+1] = alternate_phonemes
            combinations.add(''.join(copy))

        return [LanguageUtils().splitHiraganaIntoPhonemes(combination) for combination in combinations]

    def _createCombinationsUsingCombinationPhonemeRules2(self, phonemes: List[str]) -> List[List[str]]:
        print(phonemes)
        combinations: Set[str] = {''.join(phonemes)}
        character_pairs_to_change: List[(int, List[str])] = []

        for index, phoneme in enumerate(phonemes):
            phonemeA = phoneme
            phonemeB = ""
            try:
                phonemeB = phonemes[index+1]
            except:
                pass
            for rule in self.combination_phoneme_rules:
                alternate_phonemes = rule(phonemeA, phonemeB)
                if alternate_phonemes is not None:
                    character_pairs_to_change.append((index, alternate_phonemes))
        
        print(character_pairs_to_change)

        character_pairs_to_change_combinations = ListUtils().powerset(character_pairs_to_change)
        print(character_pairs_to_change_combinations)
        for combination in character_pairs_to_change_combinations:
            copy = phonemes.copy()
            # iterate in reverse order so we can change the characters without affecting index
            for index, alternate_phonemes in reversed(combination):
                if index+1 == len(phonemes):
                    copy[index:index+1] = alternate_phonemes
                else:
                    copy[index:index+2] = alternate_phonemes
            combinations.add(''.join(copy))

        return [LanguageUtils().splitHiraganaIntoPhonemes(combination) for combination in combinations]

    def _createCombinationsUsingCombinationPhonemeRules(self, phonemes: List[str]) -> List[List[str]]:
        # Ex w/ input 'sam' where there is a rule to turn 'am' into 'an'
        #  --> [[['s','a']], [['a','m'], ['a,'n']], [['m']]]
        combination_possibilities: List[List[List[str]]] = []
        for index, phoneme in enumerate(phonemes):
            all_combinations_for_index = []
            phonemeA = phoneme
            phonemeB = ""
            try:
                phonemeB = phonemes[index+1]
                #default
                all_combinations_for_index.append([phonemeA, phonemeB])
            except:
                all_combinations_for_index.append([phonemeA])
                pass
            for rule in self.combination_phoneme_rules:
                alternate_phonemes = rule(phonemeA, phonemeB)
                if alternate_phonemes is not None:
                    all_combinations_for_index.append(alternate_phonemes)
            combination_possibilities.append(all_combinations_for_index)

        # result of example input 'sam'
        # [[['s','a'], ['a,'m'], ['m']], [['s','a'], ['a,'n'], ['m']]]
        combinations = ListUtils().combination(combination_possibilities)

        combination_hiragana = [ self._merge(c) for c in combinations ]
        # remove duplicates
        combination_hiragana = list(dict.fromkeys(combination_hiragana))

        return [LanguageUtils().splitHiraganaIntoPhonemes(combination) for combination in combination_hiragana]

    def _merge(self, phoneme_pairs: List[List[str]]) -> str:
        result = ''.join(phoneme_pairs[0])
        for index in range(1, len(phoneme_pairs)):
            pair = phoneme_pairs[index]
            if self._canMerge(result, pair):
                to_add = ''.join(pair[1:])
                result += to_add
            else:
                index += 1
                if index < len(phoneme_pairs):
                    to_add = ''.join(phoneme_pairs[index])
                    result += to_add
                index += 1
        return result

    def _canMerge(self, original_string: str, pair_to_merge: List[str]) -> bool:
        return original_string[-1] == pair_to_merge[0]
