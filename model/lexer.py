# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

import jieba
import jieba.posseg

__all__ = ["Lexer"]


class Lexer(object):
    def __init__(self, **model_paths):
        self.is_init = False

        custom_dict_path = model_paths['custom_dict_path']
        if custom_dict_path and not self.is_init:
            jieba.load_userdict(custom_dict_path)

    def check(self, text):
        """
        Args:
            text: I love it
        Returns:
        {
          "text":"I love it",
          "items":[
            {
           "length":1,
           "offset":0,
           "formal":"",
           "item":"I",
           "ne":"p",
           "pos":"n",
           "uri":"",
           "loc_details":[ ],
           "basic_words":["I"]
            },
        }
        """
        result_dict = {"text": text}
        words = jieba.posseg.cut(text)
        items_list = []
        idx = 0
        for w in words:
            items = dict()
            items["item"] = w.word
            items["pos"] = w.flag
            items['length'] = len(w.word)
            items['offset'] = idx
            idx = len(w.word) + idx
            items['formal'] = ''
            items['ne'] = ''
            items['uri'] = ''
            items['loc_details'] = []
            items['basic_words'] = [w.word]
            items_list.append(items)
        result_dict['items'] = items_list
        return result_dict
