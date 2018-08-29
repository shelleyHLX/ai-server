# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import os

from imageai.Prediction import ImagePrediction

from util.io_util import get_logger

logger = get_logger(__file__)


class Prediction(object):
    model = None

    def __init__(self, model_path=None):
        self.name = 'image_prediction'
        self.model = ImagePrediction()
        self.model.setModelTypeAsResNet()
        # load model by file
        if model_path:
            try:
                pwd_path = os.path.abspath(os.path.dirname(__file__))
                model_path = os.path.join(pwd_path, '../..', model_path)
                self.model.setModelPath(model_path)
            except ValueError:
                self.model.setModelPath(model_path)
            logger.info("Load model ok, path: " + model_path)
        else:
            logger.error('model file is need.')
            raise Exception('model file need.')
        self.model.loadModel()

    @classmethod
    def get_instance(cls, model_path=None):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path)
            cls.model = obj
            return obj

    def predict_image(self, input_image_path, result_count=5):
        predictions, probabilities = self.model.predictImage(input_image_path, result_count=result_count)
        return predictions, probabilities

    def check(self, input_image_path):
        """
        Args:
            input_image_path
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
        result_dict = {"input": input_image_path}
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
