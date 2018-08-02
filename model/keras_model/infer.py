# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: infer deep model

from keras.models import load_model

from util.io_util import get_logger
from .data_reader import vectorize_words, load_dict, pad_sequence

logger = get_logger(__name__)


class InferCNN(object):
    def __init__(self, save_model_path, word_dict_path, maxlen=400):
        self.name = 'keras_infer'
        # load dict
        if word_dict_path:
            self.word_ids_dict = load_dict(word_dict_path)
        # load model by file
        if save_model_path:
            self.model = load_model(save_model_path)
            logger.debug("Load model ok, path: ", save_model_path)
        else:
            raise Exception('model file need.')
        self.maxlen = maxlen

    def infer(self, test_text):
        # read data to index
        test_text_words = [list(test_text)]
        word_ids = vectorize_words(test_text_words, self.word_ids_dict)
        # pad sequence
        word_seq = pad_sequence(word_ids, self.maxlen)
        # predict prob
        probs = self.model.predict(word_seq)
        # get prob for one line test text
        return probs[0]
