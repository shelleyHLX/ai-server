# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import base64
import os
import time

import tensorflow as tf
from imageai.Detection import ObjectDetection

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64, resize_img, rename_path

logger = get_logger(__file__)


class Detection(object):
    model = None

    def __init__(self, model_path=None):
        self.name = 'image_detection'
        self.model = ObjectDetection()
        self.model.setModelTypeAsRetinaNet()
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))
        # load parrots_model by file
        if model_path:
            try:
                model_path = os.path.join(self.pwd_path, '../..', model_path)
                self.model.setModelPath(model_path)
            except ValueError:
                self.model.setModelPath(model_path)
            logger.info("Load image_detection ok, path: " + model_path)
        else:
            logger.error('image_detection file is need')
            raise Exception('image_detection file need')
        self.model.loadModel()
        self.graph = tf.get_default_graph()

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
        with self.graph.as_default():
            detections = self.model.detectObjectsFromImage(input_image_path,
                                                           output_image_path=output_image_path,
                                                           extract_detected_objects=extract_detected_objects,
                                                           minimum_percentage_probability=minimum_percentage_probability,
                                                           display_percentage_probability=display_percentage_probability,
                                                           display_object_name=display_object_name)
        return detections

    def check_file(self, input_image_path, output_image_path=''):
        """
        Args:
            input_image_path: path(string)
            output_image_path: path(string)
        """
        result_dict = {"input_image_path": input_image_path}

        items = []
        if output_image_path:
            detections = self.detect_image(input_image_path, output_image_path=output_image_path)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'detected_' + file_name + suffix)
            detections = self.detect_image(input_image_path, output_image_path=output_image_path)
        result_dict['output_image_path'] = output_image_path
        encoded = base64.b64encode(open(output_image_path, 'rb').read())
        result_dict['output_base64'] = encoded.decode('utf-8')
        for each_detection in detections:
            # print(each_detection['name'], " : ", str(each_detection['percentage_probability']))
            item = dict()
            item['name'] = each_detection['name']
            item['score'] = float(each_detection['percentage_probability'])
            item['box_points'] = each_detection['box_points']
            items.append(item)
        result_dict['items'] = items
        return result_dict

    def check(self, input_image_base64, output_image_path=''):
        """
        Args:
            input_image_base64
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

        return self.check_file(resize_img_path, output_image_path)
