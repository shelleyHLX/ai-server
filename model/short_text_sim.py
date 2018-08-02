# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
import numpy as np

from util.io_util import get_logger
from util.math_util import cos_dist
from .word_emb import WordEmb
from .lexer import Lexer

default_logger = get_logger(__file__)



def seg(text):
    lexer_model = Lexer()
    return lexer_model.seg(text)


class ShortTextSim(WordEmb):
    def __init__(self, emb_path=None):
        super(ShortTextSim, self).__init__(emb_path)
        self.name = 'short_text_sim'

    def get_text_emb(self, text):
        words = seg(text)
        embs = []
        for word in words:
            if word in self.emb_model.vocab:
                emb = self.emb_model[word]
            else:
                emb = 0
            embs.append(emb)
        embs_array = np.array(embs)
        embs_vec = embs_array.sum(axis=0)
        return embs_vec

    def check(self, text):
        """
        Args:
            text: 浙富股份 万事通自考网
        Returns:
        {
            "log_id": 12345,
            "texts":{
                "text_1":"浙富股份",
                "text_2":"万事通自考网"
            },
            "score":0.3300237655639648 //相似度结果
        },
        """
        text = text.strip()
        words = text.split()
        if len(words) != 2:
            return
        text_1, text_2 = words[0], words[1]
        result_dict = {'texts': {'text_1': text_1, 'text_2': text_2}}
        text_emb_1 = self.get_text_emb(text_1)
        text_emb_2 = self.get_text_emb(text_2)
        cos = cos_dist(text_emb_1, text_emb_2)
        result_dict['score'] = cos
        return result_dict