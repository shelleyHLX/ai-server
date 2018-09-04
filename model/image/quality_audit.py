# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import base64
import time

import cv2

from utils.base64_util import get_suffix_base64
from utils.io_util import get_logger

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

    def check_file(self, input_image_path, clear_threshold=100):
        """
        Args:
            input_image_path: (string)
            clear_threshold
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": path
        }
        """
        result_dict = {"input_image_path": input_image_path}

        clear_score = self.variance_image(input_image_path)
        # if the focus measure is more than the supplied threshold(default:100),
        # then the image should be considered "clear"
        result_dict['clarity'] = clear_score
        if clear_score > clear_threshold:
            result_dict['output'] = 'pass'
        else:
            result_dict['output'] = 'reject'
        return result_dict

    def check(self, input_image_base64, clear_threshold=100):
        """
        Args:
            input_image_base64: (string)
            clear_threshold
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": path
        }
        """
        input_image_base64, suffix = get_suffix_base64(input_image_base64)
        input_image = base64.b64decode(input_image_base64)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        input_image_path = now + '.' + suffix
        with open(input_image_path, 'wb') as f:
            f.write(input_image)
        return self.check_file(input_image_path, clear_threshold)
