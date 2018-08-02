# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
from model import keyword

input_datas = ['此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。',
               '此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元。  增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。',
               '你好吗 我你们才是不好吗']
model = keyword.Keyword()

for input_data in input_datas:
    out = ''
    check_ret = model.check(input_data)
    print(check_ret)
    items = check_ret['items']
    for item in items:
        out += item['tag'] + ' '
    print(out)
