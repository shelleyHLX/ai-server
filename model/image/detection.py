# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import os

from imageai.Detection import ObjectDetection

from util.io_util import get_logger

logger = get_logger(__file__)


class Detection(object):
    model = None

    def __init__(self, model_path=None):
        self.name = 'image_detection'
        self.model = ObjectDetection()
        self.model.setModelTypeAsRetinaNet()
        # load model by file
        if model_path:
            try:
                self.model.setModelPath(model_path)
            except IOError:
                pwd_path = os.path.abspath(os.path.dirname(__file__))
                model_path = os.path.join(pwd_path, '../..', model_path)
                self.model.setModelPath(model_path)
            logger.info("Load model ok, path: " + model_path)
        else:
            logger.error('model file is need')
            raise Exception('model file need')
        self.model.loadModel()

    @classmethod
    def get_instance(cls, model_path=None):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path)
            cls.model = obj
            return obj

    def detect_image(self, input_image_path,
                     output_image_path='',
                     extract_detected_objects=False,
                     minimum_percentage_probability=50,
                     display_percentage_probability=True,
                     display_object_name=True):
        detections = self.model.detectObjectsFromImage(input_image_path,
                                                       output_image_path=output_image_path,
                                                       extract_detected_objects=extract_detected_objects,
                                                       minimum_percentage_probability=minimum_percentage_probability,
                                                       display_percentage_probability=display_percentage_probability,
                                                       display_object_name=display_object_name)
        return detections

    def check(self, input_image_path, output_image_path=''):
        """
        Args:
            input_image_path
            output_image_path
        Returns:
        {
            "log_id": "123",
            "items": [
                {
                    "score": 97.672176361084,
                    "name": "钟花樱桃"
                },
                {
                    "score": 1.4195868745446,
                    "name": "垂丝海棠"
                },
                {
                    "score": 0.28223067056388,
                    "name": "榆叶梅"
                },
                {
                    "score": 0.13810899108648,
                    "name": "杏"
                },
                {
                    "score": 0.10830771643668,
                    "name": "大山樱"
                }
            ]
        }
        """
        result_dict = {'input': input_image_path}
        items = []
        if output_image_path:
            detections = self.detect_image(input_image_path, output_image_path=output_image_path)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'detected_' + file_name + suffix)
            detections = self.detect_image(input_image_path, output_image_path=output_image_path)
        result_dict['output'] = output_image_path
        for each_detection in detections:
            # print(each_detection['name'], " : ", str(each_detection['percentage_probability']))
            item = dict()
            item['name'] = each_detection['name']
            item['score'] = float(each_detection['percentage_probability'])
            item['box_points'] = each_detection['box_points']
            items.append(item)
        result_dict['items'] = items
        return result_dict
