# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 图片着色
"""
import base64
import os
import time

import numpy as np
import tensorflow as tf
from keras.layers import Conv2D, UpSampling2D, InputLayer
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave

from utils.base64_util import get_suffix_base64
from utils.io_util import get_logger

logger = get_logger(__file__)


def get_train_data(img_file):
    image = img_to_array(load_img(img_file))
    image_shape = image.shape
    print(image_shape)

    image = np.array(image, dtype=float)
    x = rgb2lab(1.0 / 255 * image)[:, :, 0]
    y = rgb2lab(1.0 / 255 * image)[:, :, 1:]
    y /= 128
    x = x.reshape(1, image_shape[0], image_shape[1], 1)
    y = y.reshape(1, image_shape[0], image_shape[1], 2)
    return x, y, image_shape


def build_model():
    model = Sequential()
    model.add(InputLayer(input_shape=(None, None, 1)))
    model.add(Conv2D(8, (3, 3), activation='relu', padding='same', strides=2))
    model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same', strides=2))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same', strides=2))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
    model.compile(optimizer='adam', loss='mse')
    return model


def train(train_input_image_path, save_model_path):
    """
    训练数据
    :param train_input_image_path:
    :param save_model_path:
    :return:
    """
    x, y, img_shape = get_train_data(train_input_image_path)
    print(x, y, img_shape)
    model = build_model()
    num_epochs = 1000  # 训练次数
    batch_size = 1

    model.fit(x, y, batch_size=batch_size, epochs=num_epochs)
    model.save(save_model_path)


class Colorize(object):
    model = None

    def __init__(self, model_path):
        self.name = 'image_colorize'
        self.model = build_model()
        self.pwd_path = os.path.abspath(os.path.dirname(__file__))
        if model_path:
            try:
                model_path = os.path.join(self.pwd_path, '../..', model_path)
                self.model.load_weights(model_path)
            except ValueError:
                self.model.load_weights(model_path)
            logger.info("Load %s model ok, path: %s" % (self.name, model_path))
            self.graph = tf.get_default_graph()

    @classmethod
    def get_instance(cls, model_path):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path)
            cls.model = obj
            return obj

    def colorize_image(self, input_image_path):
        try:
            # 加载图片
            x, y, image_shape = get_train_data(input_image_path)
            with self.graph.as_default():
                predict_lab = self.model.predict(x)
            predict_lab *= 128
            predict_arr = np.zeros((200, 200, 3))
            predict_arr[:, :, 0] = x[0][:, :, 0]
            predict_arr[:, :, 1:] = predict_lab[0]
            predict_image = lab2rgb(predict_arr)
        except Exception:
            raise Exception('predict error.')
        return predict_image

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
        predict_image = self.colorize_image(input_image_path)
        if output_image_path:
            imsave(output_image_path, predict_image)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'colorized_' + file_name + suffix)
            imsave(output_image_path, predict_image)
        result_dict['output_image_path'] = output_image_path
        encoded = base64.b64encode(open(output_image_path, 'rb').read())
        result_dict['output_base64'] = encoded.decode('utf-8')
        return result_dict

    def check(self, input_image_base64, output_image_path=''):
        """
        Args:
            input_image_base64: string
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
            logger.info(input_image_path)
        return self.check_file(input_image_path, output_image_path)
