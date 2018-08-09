# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from util.io_util import get_logger
import pycorrector

default_logger = get_logger(__file__)


class Corrector(object):
    def __init__(self):
        self.name = 'corrector'
        self.model = pycorrector

    def get_corrected_text(self, text):
        return self.model.correct(text)

    def check(self, text):
        """
        Args:
            text: 少先队员因该为老人让坐
        Returns:
        {
            "text": "少先队员因该为老人让坐",
            "log_id": 3956079,
            "item": {
                "vec_fragment": [
                    {
                        "ori_frag": "因该",
                        "correct_frag": "应该",
                        "begin_pos": 4,
                        "end_pos": 6,
                        "score": 0.87
                    },
                    {
                        "ori_frag": "坐",
                        "correct_frag": "座",
                        "begin_pos": 10,
                        "end_pos": 11,
                        "score": 0.91
                    }
                ],
                "correct_query": "少先队员应该为老人让座"
            },
        }
        """
        result_dict = {"text": text}
        corrected_text = self.get_corrected_text(text)
        items_list = []
        for w, s in corrected_text:
            items = dict()
            items["score"] = s
            items["tag"] = w
            items_list.append(items)
        result_dict['items'] = items_list
        return result_dict
