"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `list`'s of items and produce vectors out of the same.
.. autoclass:: revscoring.datasources.meta.vectors
"""
import os.path

from gensim.models.keyedvectors import KeyedVectors

from ..datasource import Datasource

ASSET_SEARCH_DIRS = ["word2vec/", "~/.word2vec/", "/var/share/word2vec/"]


class word2vec(Datasource):
    """
    Generates vectors using "word2vec format" for a list of items generated
    by another datasource.
    :Parameters:
        words_datasource : :class:`revscoring.Datasource`
            A datasource that returns a list of words.
        vectorize_words : `function`
            a function that takes a list of words and converts it to a list
            of vectors of those words
        keyed_vectors : `dict`
            A list of word vectors in "word2vec format"
        name : `str`
            A name for the `revscoring.FeatureVector`
    """  # noqa

    def __init__(self, words_datasource, keyed_vectors, name=None):
        name = self._format_name(name, [words_datasource])
        self.keyed_vectors = keyed_vectors
        super().__init__(name, self.vectorize_words, depends_on=[words_datasource])

    def vectorize_words(self, words):
        list_of_vectors = [
            self.keyed_vectors[word]
            for word in words or [] if word in self.keyed_vectors]
        if len(list_of_vectors) == 0:
            list_of_vectors = [[0] * self.keyed_vectors.vector_size]
        return list_of_vectors

    @staticmethod
    def load_kv(filename=None, path=None, binary=False, limit=None):
        if path is not None:
            return KeyedVectors.load_word2vec_format(
                path, binary=binary, limit=limit)
        elif filename is not None:
            for dir_path in ASSET_SEARCH_DIRS:
                try:
                    path = os.path.join(dir_path, filename)
                    return KeyedVectors.load_word2vec_format(
                        path, binary=binary, limit=limit)
                except FileNotFoundError:
                    continue
            raise FileNotFoundError("Please make sure that 'filename' \
                                    specifies the word vector binary name \
                                    in default search paths or 'path' \
                                    speficies file path of the binary")
        else:
            raise TypeError(
                "load_kv() requires either 'filename' or 'path' to be set.")
