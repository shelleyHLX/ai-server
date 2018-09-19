# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import base64
import os
import time

import tensorflow as tf
from imageai.Prediction import ImagePrediction

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64, resize_img, rename_path

logger = get_logger(__file__)


class Prediction(object):
    model = None

    def __init__(self, model_path=None):
        self.name = 'image_prediction'
        self.model = ImagePrediction()
        self.model.setModelTypeAsResNet()
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))
        # load parrots_model by file
        if model_path:
            try:
                model_path = os.path.join(self.pwd_path, '../..', model_path)
                self.model.setModelPath(model_path)
            except ValueError:
                self.model.setModelPath(model_path)
            logger.info("Load ImagePrediction ok, path: " + model_path)
        else:
            logger.error('ImagePrediction file is need.')
            raise Exception('ImagePrediction file need.')
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

    def predict_image(self, input_image_path, result_count=5):
        with self.graph.as_default():
            predictions, probabilities = self.model.predictImage(input_image_path, result_count=result_count)
        return predictions, probabilities

    def check_file(self, input_image_path):
        """
        Args:
            input_image_path: path(string)
        """
        result_dict = {"input_image_path": input_image_path}
        items = []
        predictions, probabilities = self.predict_image(input_image_path, result_count=5)
        for each_prediction, each_probability in zip(predictions, probabilities):
            # print(each_prediction, " : ", each_probability)
            item = dict()
            item['name'] = each_prediction
            item['score'] = each_probability
            items.append(item)
        result_dict['items'] = items
        return result_dict

    def check(self, input_image_base64):
        """
        Args:
            input_image_base64
        Returns:
        {
            "log_id": "4626675444055410890",
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

        return self.check_file(resize_img_path)
