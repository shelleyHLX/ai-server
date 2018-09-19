# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
import operator
import os

import tensorflow as tf
from keras.models import load_model

from model.nlp.keras_data_reader import load_dict
from model.nlp.keras_data_reader import pad_sequence
from model.nlp.keras_data_reader import vectorize_words
from utils.io_util import get_logger

logger = get_logger(__file__)

label_revserv_dict = {0: '人类作者',
                      1: '机器作者',
                      2: '机器翻译',
                      3: '自动摘要'}


class Topic(object):
    topic_model = None

    def __init__(self, model_path, word_dict_path, maxlen=400):
        self.name = 'topic'
        self.maxlen = maxlen
        # load dict
        pwd_path = os.path.abspath(os.path.dirname(__file__))
        if word_dict_path:
            try:
                self.word_ids_dict = load_dict(word_dict_path)
            except IOError:
                word_dict_path = os.path.join(pwd_path, '../..', word_dict_path)
                self.word_ids_dict = load_dict(word_dict_path)

        # load parrots_model by file
        if model_path:
            try:
                self.topic_model = load_model(model_path)
            except IOError:
                model_path = os.path.join(pwd_path, '../..', model_path)
                self.topic_model = load_model(model_path)
            logger.info("Load topic model ok, path: " + model_path)
            # self.topic_model._make_predict_function()  # have to initialize before threading
            self.graph = tf.get_default_graph()
        else:
            logger.warn('topic model file is need')
            raise Exception('topic model file need')

    @classmethod
    def get_instance(cls, model_path, word_dict_path, maxlen=400):
        if cls.topic_model:
            return cls.topic_model
        else:
            obj = cls(model_path, word_dict_path, maxlen=maxlen)
            cls.topic_model = obj
            return obj

    def get_topic(self, text):
        # read data to index
        test_text_words = [list(text)]
        word_ids = vectorize_words(test_text_words, self.word_ids_dict)
        # pad sequence
        word_seq = pad_sequence(word_ids, self.maxlen)

        with self.graph.as_default():
            # predict prob
            predict_probs = self.topic_model.predict(word_seq)
        # get prob for one line test text
        probs = predict_probs[0]
        probs_dict = dict((idx, prob) for idx, prob in enumerate(probs))
        probs_order_dict = sorted(probs_dict.items(), key=operator.itemgetter(1), reverse=True)
        return probs_order_dict

    def check(self, text):
        """
        Args:
            text: 欧洲冠军联赛是欧洲足球协会联盟主办的年度足球比赛
        Returns:
        {
            "log_id": 3591049593939822907,
            "items": {
                "lv2_tag_list": [
                    {
                        "score": 0.877436,
                        "tag": "足球"
                    },
                    {
                        "score": 0.793682,
                        "tag": "国际足球"
                    },
                    {
                        "score": 0.775911,
                        "tag": "英超"
                    }
                ],
                "lv1_tag_list": [
                    {
                        "score": 0.824329,
                        "tag": "体育"
                    }
                ]
            }
        }
        """
        result_dict = {"text": text}
        topics = self.get_topic(text)
        items_list = []
        for idx, prob in topics:
            # get top 3
            if len(items_list) > 2:
                continue
            items = dict()
            items["score"] = prob
            items["tag"] = label_revserv_dict[idx]
            items_list.append(items)
        result_dict['items'] = items_list
        return result_dict
