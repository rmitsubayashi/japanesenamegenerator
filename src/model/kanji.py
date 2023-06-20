import json

class Pronunciation:
    def __init__(self, main: str, okurigana: str):
        self.main = main
        self.okurigana = okurigana

# multiple pronunciations for a Kanji are stored in separate objects
class Kanji:
    def __init__(self, kanji: str, pronunciation: Pronunciation):
        self.kanji = kanji
        self.pronunciation = pronunciation
        self.similarity_score = None
        self.relevant_phrases = []
        # a string indicating the exact pronunciation that fits the input name
        self.selected_pronunciation = None
        

    @staticmethod
    def from_string(json_str):
        json_dict = json.loads(json_str)
        return Kanji(json_dict["kanji"], Pronunciation(json_dict["pronunciation"]["main"], json_dict["pronunciation"]["okurigana"]))
    
    def __eq__(self, other):
        if not isinstance(other, Kanji):
            return False
        
        return self.kanji == other.kanji and self.pronunciation.main == other.pronunciation.main and self.pronunciation.okurigana == other.pronunciation.okurigana