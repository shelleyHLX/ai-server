# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 数字化妆
"""
import os

import face_recognition
from PIL import Image
from PIL import ImageDraw

from util.io_util import get_logger

logger = get_logger(__file__)


class FaceMakeup(object):
    model = None

    def __init__(self):
        self.name = 'face_makeup'
        self.model = face_recognition

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

    def check(self, input_image_path, output_image_path=''):
        """
        Args:
            input_image_path: path(string)
            output_image_path: path(string)
        Returns:
         {
            "log_id": "3586909108147953423",
            "input": path,
            "output": path
        }
        """
        result_dict = {'input': input_image_path}
        makeup_image = self.draw_image(input_image_path)
        if output_image_path:
            makeup_image.save(output_image_path)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'makeup_' + file_name + suffix)
            makeup_image.save(output_image_path)
        result_dict['output'] = output_image_path
        return result_dict
