# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import base64
import os
import time

import parrots

from utils.io_util import get_logger
from utils.string_util import rename_path

logger = get_logger(__file__)


class TTS(object):
    model = None

    def __init__(self, model_path):
        self.name = 'text_to_speech'
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(self.pwd_path, '../..', model_path)
        self.model = parrots.TextToSpeech(syllables_dir=model_path)
        logger.info("Load TextToSpeech parrots_model ok, path: " + model_path)

    @classmethod
    def get_instance(cls, model_path):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path)
            cls.model = obj
            return obj

    def text_2_speech(self, input_text, output_voc_path='out.wav'):
        """
        text to speech
        :param input_text:
        :param output_voc_path
        :return: speech file
        """
        voc = self.model.synthesize(input_text, output_voc_path)
        logger.info(output_voc_path)
        return voc

    def speak(self, input_text):
        self.model.speak(input_text)

    def check(self, input_text, output_voc_path=''):
        """
        Args:
            input_text: text
            output_voc_path: path
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": text
        }
        """
        result_dict = {'input': input_text}
        # self.speak(input_text)
        if output_voc_path:
            self.text_2_speech(input_text, output_voc_path)
        else:
            suffix = '.wav'
            now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            path = os.path.join(self.pwd_path, '../../upload/', self.name)
            if not os.path.exists(path):
                os.makedirs(path)
            output_voc_path = os.path.join(path, now + suffix)
            output_voc_path = rename_path(output_voc_path, prefix='synthesis_')
            self.text_2_speech(input_text, output_voc_path)
        with open(output_voc_path, 'rb') as voc_f:
            encoded = base64.b64encode(voc_f.read())
            result_dict['output_base64'] = encoded.decode('utf-8')
        result_dict['output_path'] = output_voc_path
        return result_dict
