import unittest

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from src.util.language_utils import LanguageUtils
from tests.util.test_utils import TestUtils

class LanguageUtilsTest(unittest.TestCase):
    # isAlphabet
    def test_is_alphabet(self):
        all_alphabet = "abcABC"
        self.assertTrue(LanguageUtils().isAlphabet(all_alphabet))

    def test_is_alphabet_mixed(self):
        mixed_alphabet = "abcあいう"
        self.assertFalse(LanguageUtils().isAlphabet(mixed_alphabet))

    def test_is_alphabet_empty(self):
        empty = ""
        self.assertFalse(LanguageUtils().isAlphabet(empty))

    def test_is_alphabet_number(self):
        numbers = "123"
        self.assertFalse(LanguageUtils().isAlphabet(numbers))

    # isJapanese
    def test_japanese(self):
        japanese = "あいうアイウ絵"
        self.assertTrue(LanguageUtils().isJapanese(japanese))

    def test_japanese_mixed(self):
        mixed = "あいうabc"
        self.assertFalse(LanguageUtils().isJapanese(mixed))

    def test_japanese_empty(self):
        empty = ""
        self.assertFalse(LanguageUtils().isJapanese(empty))

    # isHiraganaOrKatakana
    def test_hiragana_or_katakana(self):
        hiraganaKatakana = "あいうアイウ"
        self.assertTrue(LanguageUtils().isHiraganaOrKatakana(hiraganaKatakana))

    def test_hiragana_or_katakana_mixed(self):
        mixed = "あいう絵"
        self.assertFalse(LanguageUtils().isHiraganaOrKatakana(mixed))

    def test_hiragana_or_katakana_empty(self):
        empty = ""
        self.assertFalse(LanguageUtils().isHiraganaOrKatakana(empty))

    # isKanji
    def test_Kanji(self):
        kanji = "絵"
        self.assertTrue(LanguageUtils().isKanji(kanji))

    def test_kanji_mixed(self):
        mixed = "あいう絵"
        self.assertFalse(LanguageUtils().isKanji(mixed))

    def test_kanji_empty(self):
        empty = ""
        self.assertFalse(LanguageUtils().isKanji(empty))

    # convertKatakanaToKana
    def test_convert_katakana_to_kana(self):
        expected = "あいうぁぃぅ"
        katakana = "アイウァィゥ"
        self.assertEqual(expected, LanguageUtils().convertKatakanaToKana(katakana))

    def test_convert_katakana_to_kana_mixed(self):
        expected = "あいう絵"
        mixed = "アイウ絵"
        self.assertEqual(expected, LanguageUtils().convertKatakanaToKana(mixed))

    def test_convert_katakana_to_kana_whitespace(self):
        expected = "あ い う"
        whitespace = "ア イ ウ"
        self.assertEqual(expected, LanguageUtils().convertKatakanaToKana(whitespace))

    # stripWhitespace
    def test_strip_whitespace(self):
        expected = "あ"
        katakana = "　あ "
        self.assertEqual(expected, LanguageUtils().stripWhitespace(katakana))

    # findVowelIndexOfPhoneme
    def test_find_vowel_index_of_phoneme(self):
        expected = 1
        phoneme = "ぎ"
        self.assertEqual(expected, LanguageUtils().findVowelIndexOfPhoneme(phoneme))

        expected = 3
        phoneme = "へ"
        self.assertEqual(expected, LanguageUtils().findVowelIndexOfPhoneme(phoneme))

    def test_find_vowel_index_of_phoneme_exception(self):
        expected = -1
        phoneme = "ん"
        self.assertEqual(expected, LanguageUtils().findVowelIndexOfPhoneme(phoneme))

    # getVowelOFPhoneme
    def test_get_vowel_of_phoneme(self):
        expected = "い"
        phoneme = "み"
        self.assertEqual(expected, LanguageUtils().getVowelOfPhoneme(phoneme))

    # splitHiraganaIntoPhonemes
    def test_split_long_letter(self):
        expected = ['じ','い']
        hiragana = "じー"
        self.assertEqual(expected, LanguageUtils().splitHiraganaIntoPhonemes(hiragana))

    def test_split_small_letter(self):
        expected = ['じゅ']
        hiragana = "じゅ"
        self.assertEqual(expected, LanguageUtils().splitHiraganaIntoPhonemes(hiragana))

    def test_alphabet_covers_all_phonemes(self):
        foreignNames = TestUtils(self).getNames()
        for name in foreignNames:
            hiragana = LanguageUtils().convertKatakanaToKana(name)
            phonemes = LanguageUtils().splitHiraganaIntoPhonemes(hiragana)
            for phoneme in phonemes:
                self._assertPhonemeInAlphabet(phoneme)

    def _assertPhonemeInAlphabet(self, phoneme: str):
        alphabet = LanguageUtils().alphabet
        exceptionLetters = ['っ','ん','・','＝','=','じぉ','りぁ','りぉ','ちぉ','ちぁ','ゎ','きぁ','うぁ']
        exists = False
        for _, row in alphabet.items():
            if phoneme in row or phoneme in exceptionLetters:
                exists = True
                break
        
        self.assertTrue(exists, msg=f"{phoneme} not in alphabet")

    def test_extract_kanji(self):
        expected = ['安','部']
        input = "安部しゅショウ"
        self.assertEqual(expected, LanguageUtils().extractKanjis(input))
