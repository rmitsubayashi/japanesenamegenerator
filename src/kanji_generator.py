
from japanese_english_translator import JapaneseEnglishTranslator
from api.google_translate_api import GoogleTranslateApi
from model.kanji import Kanji
from error.translation_error import TranslationError
from error.validation_error import ValidationError
from relevant_phrase_finder import RelevantPhraseFinder
from kanji_name_fitter import KanjiNameFitter
from weighted_kanji_generator import WeightedKanjiGenerator
from api.kanji_db import KanjiDB
from pronunciation_combination_generator import PronunciationCombinationGenerator
import single_phoneme_rules as single_rules
import combination_phoneme_rules as combination_rules
from util.language_utils import LanguageUtils
from typing import List

class KanjiGenerator:
    def __init__(self):
        google_translate_api = GoogleTranslateApi()
        self.translator = JapaneseEnglishTranslator(google_translate_api)
        relevant_phrase_finder = RelevantPhraseFinder()
        kanji_db = KanjiDB()
        self.weighted_kanji_generator = WeightedKanjiGenerator(relevant_phrase_finder, kanji_db)
        s_rules = single_rules.getSinglePhonemeRules()
        c_rules = combination_rules.getCombinationPhonemeRules()
        self.pronunciationCombinationGenerator = PronunciationCombinationGenerator(s_rules, c_rules)

    """
    name: the user's name. assumes just one name (eg just first name, not first + last name)
    """
    def generateKanji(self, name: str, user_properties: List[str]) -> List[List[Kanji]]:
        try:
            japanese = self.translator.translateEnglishToJapanese(name)
        except ValidationError:
            print("Validation error")
            return
        except TranslationError:
            print("Translation error")
            return
        
        kanji_store = self.weighted_kanji_generator.generate_weighted_kanji(user_properties)
    
        nameFitter = KanjiNameFitter(self.pronunciationCombinationGenerator, kanji_store)

        language_utils = LanguageUtils()
        japanese_hiragana = language_utils.convertKatakanaToKana(japanese)
        return nameFitter.fit(japanese_hiragana)