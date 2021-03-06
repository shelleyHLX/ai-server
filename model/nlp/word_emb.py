# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
import os
from utils.io_util import get_logger

logger = get_logger(__file__)


def get_word2vectors(filename):
    """
    Args:
        filename: path to the gensim.word2vec bin file
    Returns:
        matrix of embeddings
    """
    try:
        # load lexer_model
        model = KeyedVectors.load_word2vec_format(filename, binary=True)
    except IOError:
        pwd_path = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(pwd_path, '../../', filename)
        model = KeyedVectors.load_word2vec_format(filename, binary=True)
    return model


def get_trimmed_glove_vectors(filename):
    """
    Args:
        filename: path to the npz file
    Returns:
        matrix of embeddings (np array)
    """
    try:
        with np.load(filename) as data:
            return data["embeddings"]
    except IOError:
        raise IOError(filename)


class WordEmb(object):
    model = None

    def __init__(self, emb_path=None):
        if emb_path:
            self.emb_model = get_word2vectors(filename=emb_path)
            logger.info('Loaded word emb from {}'.format(emb_path))
        else:
            raise Exception('need emb file.')

    @classmethod
    def get_instance(cls, emb_path=None):
        if cls.model:
            return cls.model
        else:
            obj = cls(emb_path)
            cls.model = obj
            return obj

    def get_word_emb(self, word):
        emb = 0
        if word in self.emb_model.vocab:
            emb = self.emb_model[word]
        return emb

    def check(self, word):
        """
        Args:
            word: 张飞
        Returns:
        {
          "word": "张飞",
          "vec": [
            0.233962,
            0.336867,
            ...
            0.43869,
            0.555556
          ]
        }
        """
        result_dict = {"word": word}
        word_emb = self.get_word_emb(word)
        result_dict['vec'] = word_emb
        return result_dict
