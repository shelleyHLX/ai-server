# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: speech recognition
"""

import parrots

from utils.io_util import get_logger

logger = get_logger(__file__)


class SpeechRecognition(object):
    model = None

    def __init__(self):
        self.name = 'speech_recognition'
        self.model = parrots

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def recognize_speech(self, voc_path):
        """
        recognize voc to text
        :param voc_path:
        :return:
        """
        voc_pinyins = self.model.recognize_speech_from_file(voc_path)
        logger.info(voc_pinyins)
        text = self.model.pinyin_2_hanzi(voc_pinyins)
        return text

    def check(self, voc_path):
        """
        Args:
            voc_path: path(string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": text
        }
        """
        result_dict = {'input': voc_path}
        text = self.recognize_speech(voc_path)
        result_dict['output'] = text
        return result_dict
