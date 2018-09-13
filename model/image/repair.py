# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 图片修复,水印去除
"""
import base64
import os
import time

import cv2
import numpy as np

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64, resize_img, rename_path

logger = get_logger(__file__)


class Repair(object):
    model = None

    def __init__(self):
        self.name = 'image_repair'
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

    def repair_image(self, input_image_path):
        # 加载图片
        img = self.model.imread(input_image_path)
        # hight, width, depth = img.shape[0:3]

        # 图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0
        thresh = self.model.inRange(img, np.array([240, 240, 240]), np.array([255, 255, 255]))

        # 创建形状和尺寸的结构元素
        kernel = np.ones((3, 3), np.uint8)

        # 扩张待修复区域
        mask = self.model.dilate(thresh, kernel, iterations=1)
        specular = self.model.inpaint(img, mask, 5, flags=cv2.INPAINT_TELEA)
        return specular

    def save_image(self, output_image_path, img):
        return self.model.imwrite(output_image_path, img)

    def check_file(self, input_image_path, output_image_path=''):
        """
        Args:
            input_image_path: path(string)
            output_image_path: path(string)
        Returns:
         {
            "log_id": "12345",
            "input": path,
            "output": path
        }
        """
        result_dict = {"input_image_path": input_image_path}

        predict_image = self.repair_image(input_image_path)
        if output_image_path:
            self.save_image(output_image_path, predict_image)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'repaired_' + file_name + suffix)
            self.save_image(output_image_path, predict_image)
        result_dict['output_image_path'] = output_image_path
        encoded = base64.b64encode(open(output_image_path, 'rb').read())
        result_dict['output_base64'] = encoded.decode('utf-8')
        return result_dict

    def check(self, input_image_base64, output_image_path=''):
        """
        Args:
            input_image_base64: (string)
            output_image_path: path(string)
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
