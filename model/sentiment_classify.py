# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: sentiment classification
# Attention: fix bug with use flask for multi thread keras model infer: https://github.com/keras-team/keras/issues/2397

import os

import tensorflow as tf
from keras.models import load_model

from model.keras_data_reader import load_dict
from model.keras_data_reader import pad_sequence
from model.keras_data_reader import vectorize_words
from util.io_util import get_logger

logger = get_logger(__file__)


class Sentiment(object):
    sentiment_model = None

    def __init__(self, model_path, word_dict_path, maxlen=300):
        self.name = 'sentiment_classify'
        self.maxlen = maxlen
        # load dict
        pwd_path = os.path.abspath(os.path.dirname(__file__))
        if word_dict_path:
            try:
                self.word_ids_dict = load_dict(word_dict_path)
            except IOError:
                word_dict_path = os.path.join(pwd_path, '..', word_dict_path)
                self.word_ids_dict = load_dict(word_dict_path)

        # load model by file
        if model_path:
            try:
                self.sentiment_model = load_model(model_path)
            except IOError:
                model_path = os.path.join(pwd_path, '..', model_path)
                self.sentiment_model = load_model(model_path)
            logger.info("Load model ok, path: ", model_path)
            # self.sentiment_model._make_predict_function()  # have to initialize before threading
            self.graph = tf.get_default_graph()
        else:
            logger.warn('model file is need.')
            raise Exception('model file need.')

    @classmethod
    def get_instance(cls, model_path, word_dict_path, maxlen=300):
        if cls.sentiment_model:
            return cls.sentiment_model
        else:
            obj = cls(model_path, word_dict_path, maxlen=maxlen)
            cls.sentiment_model = obj
            return obj

    def get_sentiment_prob(self, text):
        # read data to index
        test_text_words = [list(text)]
        word_ids = vectorize_words(test_text_words, self.word_ids_dict)
        # pad sequence
        word_seq = pad_sequence(word_ids, self.maxlen)
        # predict prob
        with self.graph.as_default():
            predict_probs = self.sentiment_model.predict(word_seq)
        # get prob for one line test text
        probs = predict_probs[0]
        probs_dict = dict((idx, prob) for idx, prob in enumerate(probs))
        return probs_dict

    def get_sentiment_confidence(self, pos_prob, pos_threshold=0.65, neg_threshold=0.35):
        """
        Get sentiment score
        :param pos_prob:
        :param pos_threshold:
        :param neg_threshold:
        :return: 表示情感极性分类结果，0:负向，1:中性，2:正向
        """
        if pos_prob > pos_threshold:
            sentiment = 2
            confidence = (pos_prob - pos_threshold) / (1 - pos_threshold)
        elif pos_prob < neg_threshold:
            sentiment = 0
            confidence = (neg_threshold - pos_prob) / neg_threshold
        else:
            sentiment = 1
            gap = pos_threshold - pos_prob if pos_prob > 0.5 else pos_prob - neg_threshold
            confidence = gap / (pos_threshold - 0.5)
        return sentiment, confidence

    def check(self, text):
        """
        Args:
            text: 苹果是一家伟大的公司
        Returns:
        {
            "text":"苹果是一家伟大的公司",
            "items":[
                {
                    "sentiment":2,    //表示情感极性分类结果
                    "confidence":0.40, //表示分类的置信度
                    "positive_prob":0.73, //表示属于积极类别的概率
                    "negative_prob":0.27  //表示属于消极类别的概率
                }
            ]
        }
        """
        result_dict = {"text": text}
        probs_dict = self.get_sentiment_prob(text)
        neg_prob, pos_prob = probs_dict[0], probs_dict[1]
        items = dict()
        items["positive_prob"] = pos_prob
        items["negative_prob"] = neg_prob
        items['sentiment'], items['confidence'] = self.get_sentiment_confidence(pos_prob)
        result_dict['items'] = [items]
        return result_dict
