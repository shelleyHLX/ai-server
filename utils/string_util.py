# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from PIL import Image

from utils.io_util import get_logger
import os

logger = get_logger(__file__)


def get_suffix_base64(raw_base64):
    """
    get suffix and base code
    :param raw_base64: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA
    :return: png, iVBORw0KGgoAAAANSUhEUgAA
    """
    parts = raw_base64.split(',', 1)
    code = parts[1]
    splits = parts[0].split(';')[0].split('data:')[1].split('/')
    style, suffix = splits[0], splits[1]
    return code, suffix


def resize_img(input_image_path, output_image_path, size=(200, 200)):
    img = Image.open(input_image_path)
    try:
        new_img = img.resize(size)
        new_img.save(output_image_path)
        logger.debug('resize to:' + output_image_path)
    except Exception as e:
        logger.error(e)
        raise ValueError()


def rename_path(path, prefix='pre_'):
    dir_path, file_path = os.path.split(path)
    file_name, end = os.path.splitext(file_path)
    output_path = os.path.join(dir_path, prefix + file_name + end)
    return output_path
