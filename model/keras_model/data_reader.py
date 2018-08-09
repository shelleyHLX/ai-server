# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
from keras.preprocessing import sequence
import numpy as np
from codecs import open

def vectorize_words(words, word_idx):
    inputs = []
    for word in words:
        inputs.append([word_idx[w] for w in word if w in word_idx])
    return inputs


def load_dict(dict_path):
    return dict((line.strip('\n').split("\t")[0], idx)
                for idx, line in enumerate(open(dict_path, 'r', encoding='utf-8').readlines()))


def load_reverse_dict(dict_path):
    return dict((idx, line.strip('\n').split("\t")[0])
                for idx, line in enumerate(open(dict_path, 'r', encoding='utf-8').readlines()))


def pad_sequence(word_ids, maxlen=400):
    return sequence.pad_sequences(np.array(word_ids), maxlen=maxlen)
