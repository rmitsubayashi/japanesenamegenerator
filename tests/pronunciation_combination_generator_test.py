import unittest
from typing import Callable
from typing import List

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from src import combination_phoneme_rules, single_phoneme_rules

from pronunciation_combination_generator import PronunciationCombinationGenerator
from tests.util.test_utils import TestUtils

class JapaneseEnglishTranslatorTest(unittest.TestCase):
    def setUp(self):
        self.testUtils = TestUtils(self)

    def test_merge(self):
        sut = PronunciationCombinationGenerator([],[])
        result = sut._merge([["じょ","う"],["う","じ"],["じ"]])
        self.assertEqual("じょうじ", result)

    def test_cannot_merge(self):
        sut = PronunciationCombinationGenerator([],[])
        result = sut._merge([["じょ","ー"],["う","じ"],["じ"]])
        self.assertEqual("じょーじ", result)

    def test_merge_one_letter(self):
        sut = PronunciationCombinationGenerator([],[])
        result = sut._merge([["じ"]])
        self.assertEqual("じ", result)

    def test_create_combinations(self):
        self._test(
            single_phoneme_rules.getSinglePhonemeRules(),
            combination_phoneme_rules.getCombinationPhonemeRules(),
            "じょん",
            [['じょ','ん'],['じょ','う','ん'],['じ','よ','ん'],['じ','よ','う','ん'],['じょ','ぬ'],['じ','よ','ぬ'],['じょ','う','ぬ'],['じ','よ','う','ぬ'],['じょ','お','ん'],['じょ','お','ぬ'],['じ','よ','お','ん'],['じ','よ','お','ぬ']]
        )
    
    # single phoneme rules

    def test_small_letter_can_become_letter(self):
        self._test(
            [single_phoneme_rules._ruleSmallLetterCanBecomeBigLetter],
            [],
            "じょう",
            [['じょ','う'],['じ','よ','う']]
        )

    def test_ji(self):
        self._test(
            [single_phoneme_rules._ruleJi],
            [],
            "じ",
            [['じ'],['ぢ']]
        )

    def test_ji_2(self):
        self._test(
            [single_phoneme_rules._ruleJi],
            [],
            "ぢ",
            [['じ'],['ぢ']]
        )

    def test_zu(self):
        self._test(
            [single_phoneme_rules._ruleZu],
            [],
            "づ",
            [['づ'],['ず']]
        )

    def test_zu_2(self):
        self._test(
            [single_phoneme_rules._ruleZu],
            [],
            "ず",
            [['づ'],['ず']]
        )

    def test_dh(self):
        self._test(
            [single_phoneme_rules._ruleDh, single_phoneme_rules._ruleDh2],
            [],
            "でゅ",
            [["でゅ"],['づ'],['ず']]
        )

    def test_ky(self):
        self._test(
            [single_phoneme_rules._ruleKy],
            [],
            "きゃ",
            [["きゃ"],['か']]
        )

    def test_ts(self):
        self._test(
            [single_phoneme_rules._ruleTs],
            [],
            "つぁ",
            [["つぁ"],['た']]
        )

    def test_ny(self):
        self._test(
            [single_phoneme_rules._ruleNy],
            [],
            "にゃ",
            [["にゃ"],['な']]
        )

    def test_my(self):
        self._test(
            [single_phoneme_rules._ruleMy],
            [],
            "みゃ",
            [["みゃ"],['ま']]
        )

    def test_f(self):
        self._test(
            [single_phoneme_rules._ruleF],
            [],
            "ふぁ",
            [["ふぁ"],['は']]
        )

    def test_fy(self):
        self._test(
            [single_phoneme_rules._ruleFy],
            [],
            "ふゃ",
            [["ふゃ"],['は']]
        )

    def test_ry(self):
        self._test(
            [single_phoneme_rules._ruleRy],
            [],
            "りゃ",
            [["りゃ"],['ら']]
        )

    def test_dy(self):
        self._test(
            [single_phoneme_rules._ruleDy],
            [],
            "ぢゃ",
            [["ぢゃ"],['じゃ']]
        )

    def test_gy(self):
        self._test(
            [single_phoneme_rules._ruleGy],
            [],
            "ぎゃ",
            [["ぎゃ"],['が']]
        )

    def test_by(self):
        self._test(
            [single_phoneme_rules._ruleBy],
            [],
            "びゃ",
            [["びゃ"],['ば']]
        )

    def test_py(self):
        self._test(
            [single_phoneme_rules._rulePy],
            [],
            "ぴゃ",
            [["ぴゃ"],['ぱ']]
        )

    def test_v(self):
        self._test(
            [single_phoneme_rules._ruleV],
            [],
            "ゔぁ",
            [["ゔぁ"],['ば']]
        )

    def test_vy(self):
        self._test(
            [single_phoneme_rules._ruleVy],
            [],
            "ゔゃ",
            [["ゔゃ"],['ば']]
        )

    def test_ty(self):
        self._test(
            [single_phoneme_rules._ruleTy],
            [],
            "てゃ",
            [["てゃ"],['た']]
        )

    def test_kw(self):
        self._test(
            [single_phoneme_rules._ruleKw],
            [],
            "くぁ",
            [["くぁ"],['か']]
        )

    def test_xtsu1(self):
        self._test(
            [single_phoneme_rules._ruleXtsu1],
            [],
            "っ",
            [["っ"],['つ']]
        )

    def test_xtsu2(self):
        self._test(
            [single_phoneme_rules._ruleXtsu2],
            [],
            "っ",
            [["っ"],[]]
        )

    # combination phoneme rules
    def test_extend_vowel_after_consonant_phoneme(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleExtendVowelAfterConsonantPhoneme],
            "くじ",
            [['く','じ'],['く','う','じ'],['く','じ','い'],['く','う','じ','い']]
        )

    def test_extend_vowel_after_consonant_phoneme_before_vowel(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleExtendVowelAfterConsonantPhoneme],
            "くう",
            [['く','う']]
        )

    def test_extend_vowel_after_consonant_phoneme_vowel(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleExtendVowelAfterConsonantPhoneme],
            "うう",
            [['う','う']]
        )

    def test_n_before_n_consonant_phoneme(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleNbeforeNconsonantPhoneme],
            "いぬ",
            [['い','ぬ'],['い','ん','ぬ']]
        )

    def test_n_before_n_consonant_phoneme_after_n(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleNbeforeNconsonantPhoneme],
            "んぬ",
            [['ん','ぬ']]
        )

    def test_split_n_sound_of_consonant_phoneme(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleSplitNsoundOfNConsonantPhoneme],
            "いぬ",
            [['い','ぬ'],['い','ん','う']]
        )

    def test_split_n_sound_of_consonant_phoneme_after_n(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleSplitNsoundOfNConsonantPhoneme],
            "んぬ",
            [['ん','ぬ']]
        )
    
    def test_i_after_e_sound(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleIAfterEsound],
            "えす",
            [['え','す'],['え','い','す']]
        )
    
    def test_i_after_e_sound_before_i(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleIAfterEsound],
            "えい",
            [['え','い']]
        )

    def test_u_after_o_sound(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleUAfterOsound],
            "どら",
            [['ど','ら'],['ど','う','ら']]
        )
    
    def test_u_after_o_sound_before_u(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleUAfterOsound],
            "どう",
            [['ど','う']]
        )

    def test_u_after_o_sound_before_o(self):
        self._test(
            [],
            [combination_phoneme_rules._ruleUAfterOsound],
            "どー",
            [['ど','う'],['ど','お'],['ど','お','う']]
        )
        
    def _test(self, single_rules: List[Callable[[str],str]], combination_rules: List[Callable[[str,str],str]], input: str, expected: List[List[str]]):
        result = PronunciationCombinationGenerator(single_rules, combination_rules).createCombinations(input)
        self.testUtils.assertListContentEqualIgnoringOrder(expected, result)