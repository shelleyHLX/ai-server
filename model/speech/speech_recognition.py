# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: speech recognition
"""

import base64
import os
import time

import parrots

from utils.base64_util import get_suffix_base64
from utils.io_util import get_logger

logger = get_logger(__file__)


class SpeechRecognition(object):
    model = None

    def __init__(self):
        self.name = 'speech_recognition'
        self.model = parrots
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))

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

    def check_file(self, input_voc_path):
        """
        Args:
            input_voc_path: (string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": text
        }
        """
        result_dict = {"input_voc_path": input_voc_path}

        text = self.recognize_speech(input_voc_path)
        result_dict['output'] = text
        return result_dict

    def check(self, input_voc_base64):
        """
        Args:
            input_voc_base64: (string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": text
        }
        """
        input_voc_base64, suffix = get_suffix_base64(input_voc_base64)
        input_voc = base64.b64decode(input_voc_base64)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.join(self.pwd_path, '../../upload/', self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        input_voc_path = os.path.join(path, now + '.' + suffix)
        with open(input_voc_path, 'wb') as f:
            f.write(input_voc)
        return self.check_file(input_voc_path)
