# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from model.image import repair

input_datas = [
    '../data/images/inpaint.png',
    '../data/images/text.png',
]
model = repair.Repair()

for input_data in input_datas:
    check_ret = model.check(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
