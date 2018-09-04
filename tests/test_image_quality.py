# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from model.image import quality_audit

input_datas = [
    '../data/images/clear_dog.png',
    '../data/images/blurry_dog.png',
]
model = quality_audit.QualityAduit()

for input_data in input_datas:
    check_ret = model.check_file(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
