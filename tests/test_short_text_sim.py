# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
from model import short_text_sim
import os
import config

pwd_path = os.path.abspath(os.path.dirname(__file__))
emb_path = os.path.join(pwd_path, '..', config.emb_path)
input_datas = ['你好 你不好吧', 'ss dd', '你好吗 我你们才是不好吗']
model = short_text_sim.ShortTextSim(emb_path)

for input_data in input_datas:
    out = ''
    check_ret = model.check(input_data)
    print(check_ret)
    if check_ret:
        out = 'score: ' + str(check_ret['score'])
    print(out)
