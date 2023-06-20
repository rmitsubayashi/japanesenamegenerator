import unittest
from unittest.mock import Mock

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from error.translation_error import TranslationError
from error.validation_error import ValidationError

from japanese_english_translator import JapaneseEnglishTranslator

class JapaneseEnglishTranslatorTest(unittest.TestCase):
    def test_google_translate_works(self):
        expected = "ジョン"
        input = "John"
        google_translate_api = Mock()
        google_translate_api.translate_name.return_value = expected
        translator = JapaneseEnglishTranslator(google_translate_api)

        result = translator.translateEnglishToJapanese(input)

        self.assertEqual(expected, result)

    def test_google_translate_fails(self):
        input = "untranslatable"
        google_translate_api = Mock()
        google_translate_api.translate_name.return_value = ""
        translator = JapaneseEnglishTranslator(google_translate_api)

        self.assertRaises(TranslationError,  translator.translateEnglishToJapanese, input)

    def test_already_japanese(self):
        expected = "ジョン"
        input = expected
        google_translate_api = Mock()
        translator = JapaneseEnglishTranslator(google_translate_api)

        self.assertEqual(expected, translator.translateEnglishToJapanese(input))

    def test_non_english(self):
        input = "مثيرة"
        google_translate_api = Mock()
        translator = JapaneseEnglishTranslator(google_translate_api)

        self.assertRaises(ValidationError, translator.translateEnglishToJapanese, input)


if __name__ == '__main__':
    unittest.main()