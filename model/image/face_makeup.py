# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 数字化妆
"""
import base64
import os
import time

import face_recognition
from PIL import Image
from PIL import ImageDraw

from utils.base64_util import get_suffix_base64
from utils.io_util import get_logger

logger = get_logger(__file__)


class FaceMakeup(object):
    model = None

    def __init__(self):
        self.name = 'face_makeup'
        self.model = face_recognition
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def get_instance(cls):
        if cls.model:
            return cls.model
        else:
            obj = cls()
            cls.model = obj
            return obj

    def draw_image(self, input_image_path):
        # 加载图片到numpy array
        image = self.model.load_image_file(input_image_path)
        # 标识脸部特征
        face_landmarks_list = self.model.face_landmarks(image)
        pil_image = Image.fromarray(image)
        for face_landmarks in face_landmarks_list:
            d = ImageDraw.Draw(pil_image, 'RGBA')

            # 绘制眉毛
            d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
            d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
            d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=3)
            d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=3)

            # 绘制嘴唇
            d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
            d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
            d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=5)
            d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=5)

            # 绘制眼睛
            d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
            d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

            # 绘制眼线
            d.line(
                face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]],
                fill=(0, 0, 0, 110),
                width=4)
            d.line(
                face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]],
                fill=(0, 0, 0, 110),
                width=4)
        # pil_image.show()
        return pil_image

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

        makeup_image = self.draw_image(input_image_path)
        if output_image_path:
            makeup_image.save(output_image_path)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'makeup_' + file_name + suffix)
            makeup_image.save(output_image_path)
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
            "log_id": "3586909108147953423",
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
        return self.check_file(input_image_path, output_image_path)
