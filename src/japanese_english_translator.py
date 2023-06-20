from api.google_translate_api import GoogleTranslateApi
from error.translation_error import TranslationError
from error.validation_error import ValidationError
from util.language_utils import LanguageUtils

class JapaneseEnglishTranslator:
    def __init__(self, google_translate_api: GoogleTranslateApi):
        self.google_translate_api = google_translate_api
        self.language_utils = LanguageUtils()

    """
    Description: Translates an English name to Japanese.
    Assumes one word. Inputs like 'John Smith' should be separated into 'John' and 'Smith'
    before calling this.

    Params:
        word: Word to translate. Will validate to check if English string

    Return value:
        Japanese translation. If already in Japanese, will return that instead

    Errors:
        not English: will throw Validation error
        could not translate: will throw Translation error
    """
    def translateEnglishToJapanese(self, word: str) -> str:
        if self.language_utils.isJapanese(word):
            return word

        self._validateInput(word)
        
        result = self.google_translate_api.translate_name(word)
        if not result:
            # TODO use IPAConverter to do rule-based translation as fallback
            raise TranslationError(f"could not translate {word}")

        return result

    def _validateInput(self, word: str):
        if not self.language_utils.isAlphabet(word):
            raise ValidationError(f"input {word} is not valid")
        
        
