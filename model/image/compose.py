# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 头像特效合成
"""
import base64
import os
import time

import cv2

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64, resize_img, rename_path

logger = get_logger(__file__)


class Compose(object):
    model = None

    def __init__(self, model_path, compose_image_path=''):
        self.name = 'image_compose'
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))
        if compose_image_path:
            try:
                compose_image_path = os.path.join(self.pwd_path, '../..', compose_image_path)
                self.compose_image = cv2.imread(compose_image_path)
            except IOError:
                self.compose_image = cv2.imread(compose_image_path)

        # load parrots_model by file
        if model_path:
            try:
                # OpenCV人脸识别分类器
                model_path = os.path.join(self.pwd_path, '../..', model_path)
                self.model = cv2.CascadeClassifier(model_path)
            except IOError:
                self.model = cv2.CascadeClassifier(model_path)
            logger.info("Load parrots_model ok, path: " + model_path)
        else:
            logger.warn('parrots_model file need')
            raise Exception('parrots_model file need')

    @classmethod
    def get_instance(cls, model_path, compose_image_path):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path, compose_image_path)
            cls.model = obj
            return obj

    def draw_image(self, input_image_path):
        # load image
        input_image = cv2.imread(input_image_path)
        # transform to gray
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        # face detect
        face_rects = self.model.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        # detect face if > 0
        if len(face_rects):
            for rect in face_rects:
                x, y, w, h = rect
                sp = self.compose_image.shape
                compose_img_h = int(sp[0] / sp[1] * w)
                if compose_img_h > (y - 20):
                    compose_img_h = (y - 20)
                compose_img_size = cv2.resize(self.compose_image, (w, compose_img_h), interpolation=cv2.INTER_NEAREST)
                top = (y - compose_img_h - 20)
                if top <= 0:
                    top = 0
                row, col, channel = compose_img_size.shape
                roi = input_image[top:top + row, x:x + col]

                # create a mask of logo and create its inverse mask also
                img2gray = cv2.cvtColor(compose_img_size, cv2.COLOR_RGB2GRAY)
                ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)

                # black-out the area of logo in ROI
                img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

                # take only region of logo from logo image.
                img2_fg = cv2.bitwise_and(compose_img_size, compose_img_size, mask=mask)

                # put logo in ROI and modify the main image
                dst = cv2.add(img1_bg, img2_fg)
                input_image[top:top + row, x:x + col] = dst
        return input_image

    def save_image(self, output_image_path, img):
        return cv2.imwrite(output_image_path, img)

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

        predict_image = self.draw_image(input_image_path)
        if output_image_path:
            self.save_image(output_image_path, predict_image)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'compose_' + file_name + suffix)
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

