import jaconv
import re
from typing import List

class LanguageUtils:
    def __init__(self):
        # excludes ん because it is special (no vowel after consonant)
        self.alphabet = {
            "": ["あ","い","う","え","お"],
            "k": ["か","き","く","け","こ"],
            "s": ["さ","し","す","せ","そ"],
            "t": ["た","ち","つ","て","と"],
            "n": ["な","に","ぬ","ね","の"],
            "h": ["は","ひ","ふ","へ","ほ"],
            "m": ["ま","み","む","め","も"],
            "y": ["や","","ゆ","いぇ","よ"],
            "r": ["ら","り","る","れ","ろ"],
            "w": ["わ","うぃ","","うぇ","うぉ"],
            "g": ["が","ぎ","ぐ","げ","ご"],
            "z": ["ざ","じ","ず","ぜ","ぞ"],
            "d": ["だ","ぢ","づ","で","ど"],
            "dh": ["でゃ","でぃ","でゅ","でぇ","でょ"],
            "b": ["ば","び","ぶ","べ","ぼ"],
            "p": ["ぱ","ぴ","ぷ","ぺ","ぽ"],
            "ky": ["きゃ","きぃ","きゅ","きぇ","きょ"],
            "sh": ["しゃ","しぃ","しゅ","しぇ","しょ"],
            "ch": ["ちゃ","ちぃ","ちゅ","ちぇ","ちょ"],
            "ts": ["つぁ","つぃ","","つぇ","つぉ"],
            "ny": ["にゃ","にぃ","にゅ","にぇ","にょ"],
            "hy": ["ひゃ","ひぃ","ひゅ","ひぇ","ひょ"],
            "my": ["みゃ","みぃ","みゅ","みぇ","みょ"],
            "f": ["ふぁ","ふぃ","","ふぇ","ふぉ"],
            "fy": ["ふゃ","ふぃ","ふゅ","ふぇ","ふょ"],
            "ry": ["りゃ","りぃ","りゅ","りぇ","りょ"],
            "gy": ["ぎゃ","ぎぃ","ぎゅ","ぎぇ","ぎょ"],
            "j": ["じゃ","じぃ","じゅ","じぇ","じょ"],
            "dy": ["ぢゃ","ぢぃ","ぢゅ","ぢぇ","ぢょ"],
            "by": ["びゃ","びぃ","びゅ","びぇ","びょ"],
            "py": ["ぴゃ","ぴぃ","ぴゅ","ぴぇ","ぴょ"],
            "v": ["ゔぁ","ゔぃ","ゔ","ゔぇ","ゔぉ"],
            "vy": ["ゔゃ","","ゔゅ","","ゔょ"],
            "ty": ["てゃ","てぃ","てゅ","てぇ","てょ"],
            "kw": ["くぁ","くぃ","くぅ","くぇ","くぉ"],
            "gw": ["ぐぁ","","","",""],
            "tw": ["","","とぅ","",""],
            "dw": ["","","どぅ","",""]        
        }

    def stripWhitespace(self, input: str) -> str:
        return input.strip()

    def isAlphabet(self, input: str) -> bool:
        matcher = r"^[a-zA-Z]+$"
        return bool(re.match(matcher, input))

    def isJapanese(self, input: str) -> bool:
        matcher = r"^[一-龠ぁ-んァ-ヶ]+$"
        return bool(re.match(matcher, input))

    def isHiraganaOrKatakana(self, input: str) -> bool:
        matcher = r"^[ぁ-んァ-ヶ]+$"
        return bool(re.match(matcher, input))

    def isKanji(self, input: str) -> bool:
        matcher = r"^[一-龠]+$"
        return bool(re.match(matcher, input))

    def convertKatakanaToKana(self, input: str) -> bool:
        return jaconv.kata2hira(input)

    def findVowelIndexOfPhoneme(self, phoneme: str) -> int:
        for _, phoneme_row in self.alphabet.items():
            if phoneme in phoneme_row:
                return phoneme_row.index(phoneme)
        return -1

    def getVowelOfPhoneme(self, phoneme: str) -> str:
        index = self.findVowelIndexOfPhoneme(phoneme)
        if index == -1:
            return ""
        vowels = self.alphabet[""]
        return vowels[index]

    def splitHiraganaIntoPhonemes(self, hiragana: str) -> List[str]:
        phonemes = []
        smallLetters = ['ゃ','ゅ','ょ','ぁ','ぃ','ぅ','ぇ','ぉ'] # っ is a phoneme on its own
        longLetter = 'ー'
        for c in hiragana:
            if c in smallLetters:
                last_index = len(phonemes)-1
                if last_index == -1:
                    pass
                else:
                    # treat big letter + small letter as one phoneme
                    phonemes[last_index] += c
            elif c == longLetter:
                last_index = len(phonemes)-1
                if last_index == -1:
                    pass
                else:
                    # convert long letter to corresponding vowel
                    vowel = self.getVowelOfPhoneme(phonemes[last_index])
                    phonemes.append(vowel)
            else:
                phonemes += c
        return phonemes

    def extractKanjis(self, s: str) -> List[str]:
        kanjis = []
        for c in s:
            if self.isKanji(c):
                kanjis.append(c)
        return kanjis