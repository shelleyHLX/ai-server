# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from model.nlp import corrector

input_datas = ['少先队员因该为老人让坐',
               '人公智能有希望吗']
model = corrector.Corrector()

for input_data in input_datas:
    check_ret = model.check(input_data)
    print(check_ret)
