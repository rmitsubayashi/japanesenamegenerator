from googletrans import Translator
import re

class GoogleTranslateApi:
    def __init__(self):
        self.translator = Translator()

    def translate_name(self, name: str) -> str:
        """
        Description: uses Google Translate API to translate an Engish name to Japanese

        Params: 
            name: English name to translate. Assumes English, does not validate input.
            Note that if the input is first + last name, the space will be translated to ・
            (for example John Smith -> ジョン・スミス)

        Return value: 
            Japanese translation. Depending on the input, can be kanji, hiragana, or katakana

        Error:
            Google Translate could not translate:
                returns empty string 
        """
        request_phrase = f"my name is \"{name}\""
        result = self.translator.translate(request_phrase, dest='ja', src='en')
        # result should be something like "私の名前は「name」です"
        matcher = r"「(.*?)」"
        # or "私の名前はnameです"
        matcher2 = r"私の名前は(.*?)です"
        match_result = re.search(matcher, result.text)
        if match_result is not None and len(match_result.groups()) == 1: 
            return match_result.group(1)
        
        match_result2 = re.search(matcher2, result.text)
        
        if match_result2 is not None and len(match_result2.groups()) == 1: 
            return match_result2.group(1)
        else:
            return ""