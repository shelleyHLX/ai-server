# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os

import config
from model.image import compose

pwd_path = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(pwd_path, '..', config.compose_model_path)
compose_image_path = os.path.join(pwd_path, '..', config.compose_image_path)

input_datas = [
    '../data/images/girl.png',
    '../data/images/laptop.png',
]
model = compose.Compose(model_path, compose_image_path=compose_image_path)

for input_data in input_datas:
    check_ret = model.check_file(input_data)
    print(check_ret)
    out = check_ret['output_image_path']
    print(out)
