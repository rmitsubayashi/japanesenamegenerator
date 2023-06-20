import nltk
from nltk.corpus import wordnet
from typing import List
from nltk.corpus.reader import Synset
from nltk.corpus.reader import WordNetCorpusReader
from model.relevant_phrase import RelevantPhrase

class WordNetTranslation:
    def __init__(self, translation: str, original_word: str, synset: Synset):
        self.phrase = RelevantPhrase(translation, original_word)
        # we need the synset to get similar words from a translation
        self.synset = synset 

class WordNetApi:
    def __init__(self):
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        # wordnet is a lazy class that transforms into WordNetCorpusReader.
        # no need to cast, but makes it easier to code/debug 
        # because we can view member methods at compile time rather than at run time
        self.wordnet: WordNetCorpusReader = wordnet

    def translate(self, english: str) -> List[WordNetTranslation]:
        """
        Description: uses WordNet to find the most valid synset (a group of words with similar meaning)
            for an English word and outputs all Japanese names for the synset.

        Params: 
            english: the english word to translate

        Return value:
            all Japanese translations for a synset. The synset is the most common usage noun meaning
            (even if a verb meaning is more common, the noun will be preferred)
        """
        synsets = self.wordnet.synsets(english)
        if len(synsets) == 0:
            return []
        # synsets are ordered by frequency but prioritized by part of speech (nouns first, verbs second)
        first_synset = synsets[0]
        translations = []
        # 'synset' roughly means 'synonyms' so we want to return all synonyms as the translation
        for lemma in first_synset.lemma_names("jpn"):
            translation = WordNetTranslation(lemma, english, first_synset)
            translations.append(translation)
        return translations

    def find_similar_words(self, synset: Synset) -> List[WordNetTranslation]:
        # the only property that actually can be similar word was hypernym
        # hypernym of cat => feline
        similar_synsets = synset.hypernyms()
        similar_words = []
        # 'synset' roughly means 'synonyms' so we want to return all synonyms as the translation
        for similar_synset in similar_synsets:
            synset_name = similar_synset.name().split('.')[0]
            translations = [ WordNetTranslation(lemma_name, synset_name, similar_synset) for lemma_name in similar_synset.lemma_names("jpn") ]
            similar_words.extend(translations)
        return similar_words