# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import pytesseract
from PIL import Image

from utils.io_util import get_logger

logger = get_logger(__file__)


class Ocr(object):
    model = None

    def __init__(self):
        self.name = 'text_recognition'
        self.model = pytesseract

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

    def check(self, input_image_path, lang='chi_sim'):
        """
        Args:
            input_image_path: path(string)
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
        result_dict = {'input': input_image_path}
        items = []
        detections = self.detect_image(input_image_path, lang=lang).split('\n')
        detections = [i.strip() for i in detections if i.strip()]
        result_dict['items_num'] = len(detections)
        for each_detection in detections:
            item = dict()
            item['name'] = each_detection
            item['score'] = float(99.6089) if each_detection else 0
            items.append(item)
        result_dict['items'] = items
        return result_dict
