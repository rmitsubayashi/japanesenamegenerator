from typing import Callable
from typing import List

from util.language_utils import LanguageUtils

def getSinglePhonemeRules() -> List[Callable[[str],str]]:
    return [
        _ruleSmallLetterCanBecomeBigLetter,
        _ruleJi,
        _ruleZu,
        _ruleDh,
        _ruleDh2,
        _ruleKy,
        _ruleTs,
        _ruleNy,
        _ruleMy,
        _ruleF,
        _ruleFy,
        _ruleRy,
        _ruleDy,
        _ruleGy,
        _ruleBy,
        _rulePy,
        _ruleV,
        _ruleVy,
        _ruleTy,
        _ruleKw,
        _ruleXtsu1,
        _ruleXtsu2
    ]

# じょん -> じよん
def _ruleSmallLetterCanBecomeBigLetter(phonemeA: str) -> List[str]:
    if len(phonemeA) != 2:
        return None
    small_big_letter_map = {
        "ゃ": "や",
        "ゅ": "ゆ",
        "ょ": "よ",
        "ぃ": "い",
        "ぅ": "う",
        "ぇ": "え",
        "ぉ": "お"
    }
    for small, big in small_big_letter_map.items():
        if small in phonemeA:
            return [phonemeA[0],big]
    return None

# じ -> ぢ and ぢ -> じ
def _ruleJi(phonemeA: str) -> List[str]:
    if phonemeA == "じ":
        return ["ぢ"]
    if phonemeA == "ぢ":
        return ["じ"]
    return None

# づ -> ず and ず -> づ
def _ruleZu(phonemeA: str) -> List[str]:
    if phonemeA == "づ":
        return ["ず"]
    if phonemeA == "ず":
        return ["づ"]
    return None

# でゃ -> だ
def _ruleDh(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["dh"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["d"][index]]
    return None

# でぃ -> じ
def _ruleDh2(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["dh"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        if index == 1:
            return ["じ"]
        if index == 2:
            return ["ず"]
    return None

# きゃ -> か
def _ruleKy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["ky"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["k"][index]]
    return None

# つぁ -> た
def _ruleTs(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["ts"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["t"][index]]
    return None

# にゃ -> な
def _ruleNy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["ny"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["n"][index]]
    return None

# みゃ -> ま    
def _ruleMy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["my"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["m"][index]]
    return None

# ふぁ -> は
def _ruleF(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["f"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["h"][index]]
    return None

# ふゃ -> は
def _ruleFy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["fy"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["h"][index]]
    return None

# りゃ -> ら
def _ruleRy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["ry"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        if index in [0,1,3]:
            return [LanguageUtils().alphabet["r"][index]]
    return None

# ぎゃ -> が        
def _ruleGy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["gy"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["g"][index]]
    return None

# ぢゃ -> じゃ
def _ruleDy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["dy"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["j"][index]]
    return None

# ぎゃ -> が
def _ruleGy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["gy"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["g"][index]]
    return None

# びゃ -> ば
def _ruleBy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["by"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["b"][index]]
    return None

# ぴゃ -> ぱ
def _rulePy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["py"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["p"][index]]
    return None

# ゔぁ -> ば
def _ruleV(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["v"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["b"][index]]
    return None

# ゔゃ -> ば
def _ruleVy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["vy"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["b"][index]]
    return None

# てゃ -> た
def _ruleTy(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["ty"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["t"][index]]
    return None

# くぁ -> か
def _ruleKw(phonemeA: str) -> List[str]:
    if phonemeA in LanguageUtils().alphabet["kw"]:
        index = LanguageUtils().findVowelIndexOfPhoneme(phonemeA)
        return [LanguageUtils().alphabet["k"][index]]
    return None

# っ -> つ
def _ruleXtsu1(phonemeA: str) -> List[str]:
    if phonemeA == "っ":
        return ["つ"]
    return None

# っ -> ""
def _ruleXtsu2(phonemeA: str) -> List[str]:
    if phonemeA == "っ":
        return []
    return None