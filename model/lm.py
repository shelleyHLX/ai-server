# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

import kenlm
from util.io_util import get_logger
from .lexer import Lexer
import os

default_logger = get_logger(__file__)


class LM(Lexer):
    model = None

    def __init__(self, language_model_path=None):
        super(LM, self).__init__()
        self.name = 'lm'
        if language_model_path:
            try:
                self.model = kenlm.Model(language_model_path)
            except IOError:
                pwd_path = os.path.abspath(os.path.dirname(__file__))
                language_model_path = os.path.join(pwd_path, '..', language_model_path)
                self.model = kenlm.Model(language_model_path)
            default_logger.info('Loaded language lexer_model from {}'.format(language_model_path))
        else:
            raise Exception('lm lexer_model need.')

    @classmethod
    def get_instance(cls, language_model_path=None):
        if cls.model:
            return cls.model
        else:
            obj = cls(language_model_path)
            cls.model = obj
            return obj

    def get_ngram_score(self, words):
        """
        取n元文法得分
        :param words: list, 以词或字切分
        :param mode:
        :return:
        """
        return self.model.score(' '.join(words), bos=False, eos=False)

    def get_ppl_score(self, words):
        """
        取语言模型困惑度得分，越小句子越通顺
        :param words: list, 以词或字切分
        :param mode:
        :return:
        """
        return self.model.perplexity(' '.join(words))

    def check(self, text):
        """
        Args:
            text: 床前明月光
        Returns:
        {
          "text": "床前明月光",
          "items": [
            {
              "word": "床",
              "prob": 0.0000385273
            },
            {
              "word": "前",
              "prob": 0.0289018
            },
            {
              "word": "明月",
              "prob": 0.0284406
            },
            {
              "word": "光",
              "prob": 0.808029
            }
          ],
          "ppl": 79.0651
        }
        """
        result_dict = {"text": text}
        # get ppl with char segment
        ppl_score = self.get_ppl_score(list(text))
        items_list = []
        for w in self.seg(text):
            items = dict()
            items["word"] = w
            items["prob"] = self.get_ngram_score(w)
            items_list.append(items)
        result_dict['items'] = items_list
        result_dict['ppl'] = ppl_score
        return result_dict
