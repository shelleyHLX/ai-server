# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
import os

import config
from model.nlp import topic

pwd_path = os.path.abspath(os.path.dirname(__file__))
topic_model_path = os.path.join(pwd_path, '..', config.topic_model_path)
topic_word_dict_path = os.path.join(pwd_path, '..', config.topic_word_dict_path)

input_datas = ['此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。',
               '此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元。  增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。',
               '你好吗 我你们才是不好吗']
model = topic.Topic(topic_model_path, topic_word_dict_path)

for input_data in input_datas:
    out = ''
    check_ret = model.check(input_data)
    print(check_ret)
    items = check_ret['items']
    for item in items:
        out += item['tag'] + '/' + str(item['score']) + ' '
    print(out)
