import gensim
from typing import List


class Word2VecApi:
    def __init__(self):
        print("building word vector")
        # since the original Google News model is too large for PythonAnywhere's free plan (1.5GB),
        # we use a slim model made here https://github.com/eyaler/word2vec-slim
        self.model = gensim.models.KeyedVectors.load_word2vec_format("data/GoogleNews-vectors-negative300-SLIM.bin.gz", binary=True)
        print("done building")
    
    """
    Description: uses Word2Vec to find the 10 most similar vectors (words)

    Params:
        word: word to find similar words for in English

    Return Value:
        list of similar words in English
    """
    def find_similar_words(self, word: str) -> List[str]:
        try:
            similar_word_tuples = self.model.most_similar(positive=[word], topn=10)
        except KeyError:
            return []
        # looks like [('vehicle', 0.7821096181869507), ('cars', 0.7423831224441528)]
        # todo consider threshold
        similar_words = [sw[0] for sw in similar_word_tuples]
        # spaces are replaced by underlines (ex pickup_truck)
        return [sw.replace('_', ' ') for sw in similar_words]