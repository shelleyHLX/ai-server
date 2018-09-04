# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""


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