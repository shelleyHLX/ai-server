# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from model.image import face_makeup

input_datas = [
    '../data/images/girl.png',
    '../data/images/laptop.png',
]
model = face_makeup.FaceMakeup()

for input_data in input_datas:
    check_ret = model.check(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
