# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
import numpy as np

from utils.math_util import cos_dist
from .word_emb import WordEmb


class WordEmbSim(WordEmb):
    model = None

    def __init__(self, emb_path=None):
        super(WordEmbSim, self).__init__(emb_path)
        self.name = 'word_emb_sim'

    @classmethod
    def get_instance(cls, emb_path=None):
        if cls.model:
            return cls.model
        else:
            obj = cls(emb_path)
            cls.model = obj
            return obj

    def check(self, text):
        """
        Args:
            text: 北京 上海
        Returns:
        {
            "score": 0.456862,
            "words": {
              "word_1": "北京",
              "word_2": "上海"
            }
        }
        """
        text = text.strip()
        words = text.split()
        if len(words) != 2:
            return
        word_1, word_2 = words[0], words[1]
        result_dict = {'words': {'word_1': word_1, 'word_2': word_2}}
        word_emb_1 = self.get_word_emb(word_1)
        word_emb_2 = self.get_word_emb(word_2)
        emb_1 = np.array(word_emb_1)
        emb_2 = np.array(word_emb_2)
        cos = cos_dist(emb_1, emb_2)
        result_dict['score'] = cos
        return result_dict
