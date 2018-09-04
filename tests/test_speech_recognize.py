# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from model.speech import speech_recognition

input_datas = [
    '../data/speechs/16k.wav',
]
model = speech_recognition.SpeechRecognition()

for input_data in input_datas:
    check_ret = model.check_file(input_data)
    print(check_ret)
    out = check_ret['output']
    print(out)
