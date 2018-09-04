# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from model.image import ocr

input_datas = [
    '../data/images/text.png',
    '../data/images/laptop.png',
]
model = ocr.Ocr()

for input_data in input_datas:
    out = ''
    check_ret = model.check_file(input_data)
    print(check_ret)
    items = check_ret['items']
    for item in items:
        out += item['name'] + '/' + str(item['score']) + ' '
    print(out)
