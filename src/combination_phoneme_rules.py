from typing import Callable
from typing import List

from util.language_utils import LanguageUtils

def getCombinationPhonemeRules() -> List[Callable[[str,str],str]]:
    return [
        _ruleExtendVowelAfterConsonantPhoneme,
        _ruleNbeforeNconsonantPhoneme,
        _ruleSplitNsoundOfNConsonantPhoneme,
        _ruleIAfterEsound,
        _ruleUAfterOsound
    ]

# くりす -> くうりす
def _ruleExtendVowelAfterConsonantPhoneme(phonemeA: str, phonemeB: str) -> List[str]:
    vowels = LanguageUtils().alphabet[""]
    # あこ should not be ああこ
    if phonemeA in vowels:
        return None
    vowel_index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
    if vowel_index == -1:
        return None
    vowel = vowels[vowel_index]
    # くう should not be くうう
    if vowel == phonemeB:
        return None
    
    return [phonemeA,vowel,phonemeB]
    
# けにー -> けんにー
def _ruleNbeforeNconsonantPhoneme(phonemeA: str, phonemeB: str) -> List[str]:
    # んの should not be んんの
    if phonemeA == "ん":
        return None
    n_consonant_phonemes = LanguageUtils().alphabet["n"]
    if phonemeB in n_consonant_phonemes:
        return [phonemeA,"ん",phonemeB]

    return None

# けにー -> けんいー
def _ruleSplitNsoundOfNConsonantPhoneme(phonemeA: str, phonemeB: str) -> List[str]:
    # んの should not be んんの
    if phonemeA == "ん":
        return None
    
    n_consonant_phonemes = LanguageUtils().alphabet["n"]
    if phonemeB in n_consonant_phonemes:
        vowels = LanguageUtils().alphabet[""]
        vowel_index = n_consonant_phonemes.index(phonemeB)
        vowel = vowels[vowel_index]
        return [phonemeA,"ん",vowel]

    return None

# める -> めいる
# this rule is more so more kanji match (a lot of kanjis have 'ei' pronunciation)
def _ruleIAfterEsound(phonemeA: str, phonemeB: str) -> List[str]:
    if phonemeB == "い":
        return None

    index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
    if index == 3:
        return [phonemeA,"い",phonemeB]
    return None

# どいる -> どういる
# this rule is more so more kanji match (a lot of kanjis have 'ou' pronunciation)
def _ruleUAfterOsound(phonemeA: str, phonemeB: str) -> List[str]:
    if phonemeB == "う":
        return None

    index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
    if index != 4:
        return None
    
    if phonemeB == "お":
        return [phonemeA,"う"]
    return [phonemeA,"う",phonemeB]