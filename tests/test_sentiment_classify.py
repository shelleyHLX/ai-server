# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
import os

import config
from model.nlp import sentiment_classify

pwd_path = os.path.abspath(os.path.dirname(__file__))
topic_model_path = os.path.join(pwd_path, '..', config.sentiment_model_path)
topic_word_dict_path = os.path.join(pwd_path, '..', config.sentiment_word_dict_path)

input_datas = ['这家的餐馆好吃吗',
               '不错，在同等档次酒店中应该	值得推荐的！',
               '房间比较差，尤其是洗手间，房间隔音和餐饮服务都不好	。',
               '你好吗 我你们才是不好吗']
model = sentiment_classify.Sentiment(topic_model_path, topic_word_dict_path)

for input_data in input_datas:
    out = ''
    check_ret = model.check(input_data)
    print(check_ret)
    items = check_ret['items']
    for item in items:
        out += str(item['positive_prob']) + '/' + str(item['negative_prob']) + ' '
    print(out)
