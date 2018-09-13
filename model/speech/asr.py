# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import base64
import os
import time

import keras
import parrots

from utils.io_util import get_logger
from utils.string_util import get_suffix_base64

logger = get_logger(__file__)


pwd_path = os.path.abspath(os.path.dirname(__file__))
name = 'asr'


def recognize_speech(voc_path):
    """
    recognize voc to text
    :param voc_path:
    :return:
    """
    voc_pinyins = parrots.recognize_speech_from_file(voc_path)
    logger.info(voc_pinyins)
    text = parrots.pinyin_2_hanzi(voc_pinyins)
    return text


def check_file(input_voc_path):
    """
    Args:
        input_voc_path: (string)
    Returns:
     {
        "log_id": "12345",
        "input": path,
        "output": text
    }
    """
    result_dict = {"input_voc_path": input_voc_path}

    text = recognize_speech(input_voc_path)
    result_dict['output'] = text
    return result_dict


def check(input_voc_base64):
    """
    Args:
        input_voc_base64: (string)
    Returns:
     {
        "log_id": "12345",
        "input": path,
        "output": text
    }
    """
    keras.backend.clear_session()
    input_voc_base64, suffix = get_suffix_base64(input_voc_base64)
    input_voc = base64.b64decode(input_voc_base64)
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    path = os.path.join(pwd_path, '../../upload/', name)
    if not os.path.exists(path):
        os.makedirs(path)
    input_voc_path = os.path.join(path, now + '.' + suffix)
    with open(input_voc_path, 'wb') as f:
        f.write(input_voc)
    return check_file(input_voc_path)
