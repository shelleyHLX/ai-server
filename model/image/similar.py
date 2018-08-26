# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 图像相似度计算
"""
import cv2
import numpy as np

from util.io_util import get_logger
from util.math_util import hamming_distance

logger = get_logger(__file__)


class Similar(object):
    model = None

    def __init__(self):
        self.name = 'image_similar'
        self.model = cv2

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

    def check(self, input_image_path1, input_image_path2):
        """
        Args:
            input_image_path1: path(string)
            output_image_path2: path(string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": path
        }
        """
        result_dict = {'input1': input_image_path1, 'input2': input_image_path2}
        similar_score = self.sim_score(input_image_path1, input_image_path2)
        result_dict['score'] = similar_score
        return result_dict
