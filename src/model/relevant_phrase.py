class RelevantPhrase:
    def __init__(self, japanese: str, english: str):
        self.japanese = japanese
        self.english = english

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RelevantPhrase):
            return other.japanese == self.japanese and other.english == self.english
        return False
    
    def __hash__(self) -> int:
        return hash(self.japanese + self.english)