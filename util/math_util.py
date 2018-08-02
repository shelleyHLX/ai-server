# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

import numpy as np


def cos_dist(emb_1, emb_2):
    """
    calc cos distance
    :param emb_1: numpy.array
    :param emb_2: numpy.array
    :return: cos score
    """
    num = float(np.sum(emb_1 * emb_2))
    denom = np.linalg.norm(emb_1) * np.linalg.norm(emb_2)
    cos = num / denom if denom > 0 else 0.0
    return cos


def cos_dist2(a, b):
    """
    cos distance
    :param a: numpy.array
    :param b: numpy.array
    :return: cos score
    """
    if a.shape != b.shape or not a.shape:
        return 0.0
    up, a_sqrt, b_sqrt = 0, 0, 0
    for aa, bb in zip(a, b):
        up += aa * bb
        a_sqrt += aa ** 2
        b_sqrt += bb ** 2
    down = np.sqrt(a_sqrt * b_sqrt)
    return up / down if down > 0 else 0.0
