# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from model.image import compare

input_datas = [
    ('../data/images/clear_dog.png', '../data/images/blurry_dog.png',),
    ('../data/images/grassland1.jpeg', '../data/images/grassland2.jpeg'),
]
model = compare.Compare()

for input_data in input_datas:
    check_ret = model.check(input_data[0], input_data[1])
    print(check_ret)
    out = check_ret['score']
    print(out)
