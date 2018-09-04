# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 图像对比，图像相似度计算
"""
import base64
import os
import time

import cv2
import numpy as np

from utils.base64_util import get_suffix_base64
from utils.io_util import get_logger
from utils.math_util import hamming_distance

logger = get_logger(__file__)


class Compare(object):
    model = None

    def __init__(self):
        self.name = 'image_compare'
        self.model = cv2
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def pHash(self, image):
        """
        phash
        :param image:
        :return:
        """
        image = self.model.resize(image, (32, 32))
        gray = self.model.cvtColor(image, self.model.COLOR_BGR2GRAY)
        # 将灰度图转为浮点型，再进行dct变换
        dct = self.model.dct(np.float32(gray))
        # 取左上角的8*8，这些代表图片的最低频率
        # 这个操作等价于c++中利用opencv实现的掩码操作
        # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
        dct_roi = dct[0:8, 0:8]
        return self.get_hash(dct_roi)

    def get_hash(self, image):
        """
        输入灰度图，返回hash
        :param image: gray image
        :return:
        """
        average = np.mean(image)
        hash = []
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] > average:
                    hash.append(1)
                else:
                    hash.append(0)
        return hash

    def sim_score(self, input_image1, input_image2):
        img1 = self.model.imread(input_image1)
        img2 = self.model.imread(input_image2)
        img_hash1, img_hash2 = self.pHash(img1), self.pHash(img2)
        distance = hamming_distance(img_hash1, img_hash2)
        score = (8 * 8 - distance) / (8 * 8)
        return score

    def check_file(self, input_image1_path, input_image2_path):
        """
        Args:
            input_image1_path: (string)
            input_image2_path: (string)
        """
        result_dict = {"input_image1_path": input_image1_path,
                       'input_image2_path': input_image2_path}
        similar_score = self.sim_score(input_image1_path, input_image2_path)
        result_dict['score'] = similar_score
        return result_dict

    def check(self, input_images_base64):
        """
        Args:
            input_images_base64: (string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "score": score
        }
        """
        input_images_base64 = input_images_base64.split('\t')
        if len(input_images_base64) == 2:
            input_image1_base64 = input_images_base64[0]
            input_image2_base64 = input_images_base64[1]
        else:
            return None

        input_image1_base64, suffix1 = get_suffix_base64(input_image1_base64)
        input_image1 = base64.b64decode(input_image1_base64)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.join(self.pwd_path, '../../upload/', self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        input_image1_path = os.path.join(path, now + '.' + suffix1)
        with open(input_image1_path, 'wb') as f:
            f.write(input_image1)

        input_image2_base64, suffix2 = get_suffix_base64(input_image2_base64)
        input_image2 = base64.b64decode(input_image2_base64)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        input_image2_path = os.path.join(path, now + '.' + suffix2)
        with open(input_image2_path, 'wb') as f:
            f.write(input_image2)

        return self.check_file(input_image1_path, input_image2_path)
