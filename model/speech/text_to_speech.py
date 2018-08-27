# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os
import time

import parrots

from util.io_util import get_logger

logger = get_logger(__file__)


class TextToSpeech(object):
    model = None

    def __init__(self, model_path):
        self.name = 'text_to_speech'
        self.model = parrots.TextToSpeech(syllables_dir=model_path)

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
        self.model.synthesize(input_text, output_voc_path)
        logger.info(output_voc_path)

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
        self.speak(input_text)
        if output_voc_path:
            self.text_2_speech(input_text, output_voc_path)
        else:
            suffix = '.wav'
            output_voc_path = os.path.join('synthesis_' + input_text[:2] + str(time.time())[-3:] + suffix)
            self.text_2_speech(input_text, output_voc_path)
        result_dict['output'] = output_voc_path
        return result_dict
