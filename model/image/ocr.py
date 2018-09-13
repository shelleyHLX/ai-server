# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import base64
import os
import time

import pytesseract
from PIL import Image

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64, resize_img, rename_path

logger = get_logger(__file__)


class Ocr(object):
    model = None

    def __init__(self):
        self.name = 'text_recognition'
        self.model = pytesseract
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def detect_image(self, input_image_path, lang='chi_sim'):
        return self.model.image_to_string(Image.open(input_image_path), lang=lang).strip()

    def check_file(self, input_image_path, lang='chi_sim'):
        """
        Args:
            input_image_path: path(string)
            lang: language
        """
        result_dict = {"input_image_path": input_image_path}

        items = []
        detections = self.detect_image(input_image_path, lang=lang).split('\n')
        detections = [i.strip() for i in detections if i.strip()]
        result_dict['items_num'] = len(detections)
        for each_detection in detections:
            item = dict()
            item['name'] = each_detection
            item['score'] = float(99.1111) if each_detection else 0
            items.append(item)
        result_dict['items'] = items
        return result_dict

    def check(self, input_image_base64, lang='chi_sim'):
        """
        Args:
            input_image_base64: (string)
            lang: language
        Returns:
         {
            "log_id": "3586909108147953423",
            "items_num": 2,
            "items": [
                {
                    "score": 99.6089,
                    "name": "负债和所有者权益"
                },
                {
                    "score": 99.6365,
                    "name": "权益"
                }
            ]
        }
        """
        input_image_base64, suffix = get_suffix_base64(input_image_base64)
        input_image = base64.b64decode(input_image_base64)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.join(self.pwd_path, '../../upload/', self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        input_image_path = os.path.join(path, now + '.' + suffix)
        with open(input_image_path, 'wb') as f:
            f.write(input_image)
            logger.debug(input_image_path)
        resize_img_path = rename_path(input_image_path, prefix='resize_')
        resize_img(input_image_path, resize_img_path)

        return self.check_file(resize_img_path, lang)
