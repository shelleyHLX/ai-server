# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

import pycorrector


class Corrector(object):
    model = None

    def __init__(self):
        self.name = 'corrector'
        self.model = pycorrector

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def get_corrected_text(self, text):
        corrected_text, detail = self.model.correct(text)
        return corrected_text, detail

    def check(self, text):
        """
        Args:
            text: 少先队员因该为老人让坐
        Returns:
        {
            "text": "少先队员因该为老人让坐",
            "log_id": 3956079,
            "items": {
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
            },
            "corrected_text": "少先队员应该为老人让座"
        }
        """
        result_dict = {"text": text}
        corrected_text, detail = self.get_corrected_text(text)
        result_dict['items'] = detail
        result_dict['corrected_text'] = corrected_text
        return result_dict
