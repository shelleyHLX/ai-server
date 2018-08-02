# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from util.io_util import get_logger
from .lexer import Lexer
from gensim import corpora
from gensim import models
import numpy as np

default_logger = get_logger(__file__)


class Topic(Lexer):
    def __init__(self, lda_path=None):
        super(Topic, self).__init__()
        if lda_path:
            self.model = models.LdaModel.load(fname=lda_path)
            default_logger.info('Loaded lda model from {}'.format(lda_path))
        else:
            raise Exception('need lda model file.')
        self.name = 'topic'

    def get_topic(self, text):
        topics = []
        words = self.lexer_model.lcut(text)

        return topics

    def check(self, text):
        """
        Args:
            text: 欧洲冠军联赛是欧洲足球协会联盟主办的年度足球比赛
        Returns:
        {
            "log_id": 3591049593939822907,
            "item": {
                "lv2_tag_list": [
                    {
                        "score": 0.877436,
                        "tag": "足球"
                    },
                    {
                        "score": 0.793682,
                        "tag": "国际足球"
                    },
                    {
                        "score": 0.775911,
                        "tag": "英超"
                    }
                ],
                "lv1_tag_list": [
                    {
                        "score": 0.824329,
                        "tag": "体育"
                    }
                ]
            }
        }
        """
        result_dict = {"text": text}
        keywords = self.get_topic(text)
        items_list = []
        for w, s in keywords:
            items = dict()
            items["score"] = s
            items["tag"] = w
            items_list.append(items)
        result_dict['items'] = items_list
        return result_dict
