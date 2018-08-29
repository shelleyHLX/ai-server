# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import cv2

from util.io_util import get_logger

logger = get_logger(__file__)


class QualityAduit(object):
    model = None

    def __init__(self):
        self.name = 'quality_audit'
        self.model = cv2

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def variance_image(self, input_image_path):
        # load image
        image = self.model.imread(input_image_path)
        # to gray
        gray = self.model.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        variance = self.model.Laplacian(gray, cv2.CV_64F).var()
        return variance

    def check(self, input_image_path, clear_threshold=100):
        """
        Args:
            input_image_path: path(string)
            clear_threshold
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": path
        }
        """
        result_dict = {'input': input_image_path}
        clear_score = self.variance_image(input_image_path)
        # if the focus measure is more than the supplied threshold(default:100),
        # then the image should be considered "clear"
        result_dict['clarity'] = clear_score
        if clear_score > clear_threshold:
            result_dict['output'] = 'pass'
        else:
            result_dict['output'] = 'reject'
        return result_dict
