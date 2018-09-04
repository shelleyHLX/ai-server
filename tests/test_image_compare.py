# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from model.image import compare

input_datas = [
    ('../data/images/clear_dog.png', '../data/images/blurry_dog.png',),
    ('../data/images/grassland1.jpeg', '../data/images/grassland2.jpeg'),
    ('../data/images/grassland1.jpeg', '../data/images/grassland2.jpeg', '../data/images/blurry_dog.png',),
]
model = compare.Compare()

for input_data in input_datas:
    check_ret = model.check_file(input_data)
    print(check_ret)
