# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import os

import config
from model.image import detection

pwd_path = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(pwd_path, '..', config.image_detection)

input_datas = [
    '../data/images/red_car.png',
    '../data/images/laptop.png',
]
model = detection.Detection(model_path)

for input_data in input_datas:
    out = ''
    check_ret = model.check_file(input_data)
    print(check_ret)
    items = check_ret['items']
    for item in items:
        out += item['name'] + '/' + str(item['score']) + ' '
    print(out)
