# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from util.io_util import get_logger
from model.lexer import Lexer

default_logger = get_logger(__file__)


class Keyword(Lexer):
    model = None

    def __init__(self):
        super(Keyword, self).__init__()
        self.name = 'keyword'

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def get_keywords(self, text, use_textrank=True):
        if use_textrank:
            keywords = self.lexer_model_analyse.textrank(text, withWeight=True, topK=5)
        else:
            keywords = self.lexer_model_analyse.extract_tags(text, withWeight=True, topK=5)
        return keywords

    def check(self, text):
        """
        Args:
            text: iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下
        Returns:
        {
            "log_id": 4457308639853058292,
            "items": [
                {
                    "score": 0.997762,
                    "tag": "iphone"
                },
                {
                    "score": 0.861775,
                    "tag": "手机"
                },
                {
                    "score": 0.845657,
                    "tag": "苹果"
                },
                {
                    "score": 0.83649,
                    "tag": "苹果公司"
                },
                {
                    "score": 0.797243,
                    "tag": "数码"
                }
            ]
        }
        """
        result_dict = {"text": text}
        keywords = self.get_keywords(text, use_textrank=True)
        items_list = []
        for w, s in keywords:
            items = dict()
            items["score"] = s
            items["tag"] = w
            items_list.append(items)
        result_dict['items'] = items_list
        return result_dict
