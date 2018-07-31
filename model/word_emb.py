# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

import numpy as np
from util.io_util import get_logger

default_logger = get_logger(__file__)


class WordEmb(object):
    def __init__(self, emb_path=None):
        if emb_path:
            self.model = self.get_trimmed_glove_vectors(filename=emb_path)
            default_logger.info('Loaded word emb from {}'.format(emb_path))
        else:
            raise Exception('need emb file.')

    @staticmethod
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

    def get_word_emb(self, word):
        return [1, 1, 1, 1]

    def check(self, text):
        """
        Args:
            text: 张飞
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
        result_dict = {"word": text}
        word_emb = self.get_word_emb(text)
        result_dict['vec'] = word_emb
        return result_dict
