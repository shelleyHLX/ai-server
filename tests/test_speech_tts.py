# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from model.speech import text_to_speech

input_datas = [
    '你好北京，我爱你北京',
    '内好广州，我爱你广州123天'
]
model = text_to_speech.TextToSpeech(model_path='../data/syllables')

for input_data in input_datas:
    check_ret = model.check(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
