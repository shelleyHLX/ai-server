# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 图片着色
"""

import os

import numpy as np
from keras.layers import Conv2D, UpSampling2D, InputLayer
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave

from util.io_util import get_logger

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
        self.model.load_weights(model_path)

    @classmethod
    def get_instance(cls, model_path):
        if cls.model:
            return cls.model
        else:
            obj = cls(model_path)
            cls.model = obj
            return obj

    def colorize_image(self, input_image_path):
        # 加载图片
        x, y, image_shape = get_train_data(input_image_path)
        predict_lab = self.model.predict(x)
        predict_lab *= 128
        predict_arr = np.zeros((200, 200, 3))
        predict_arr[:, :, 0] = x[0][:, :, 0]
        predict_arr[:, :, 1:] = predict_lab[0]
        predict_image = lab2rgb(predict_arr)
        return predict_image

    def check(self, input_image_path, output_image_path=''):
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
        result_dict = {'input': input_image_path}
        predict_image = self.colorize_image(input_image_path)
        if output_image_path:
            imsave(output_image_path, predict_image)
        else:
            dir_path, file_path = os.path.split(input_image_path)
            file_name, suffix = os.path.splitext(file_path)
            output_image_path = os.path.join(dir_path, 'colorized_' + file_name + suffix)
            imsave(output_image_path, predict_image)
        result_dict['output'] = output_image_path
        return result_dict
