# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os

import config
from model.image import colorize

pwd_path = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(pwd_path, '..', config.colorize_model_path)

input_datas = [
    '../data/images/colorize2.png',
    '../data/images/colorize3.png',
]
model = colorize.Colorize(model_path)

for input_data in input_datas:
    check_ret = model.check(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
