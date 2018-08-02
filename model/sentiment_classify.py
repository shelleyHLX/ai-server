# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

import numpy as np

from model.keras_model.infer import InferCNN
from util.io_util import get_logger

default_logger = get_logger(__file__)


class Sentiment(InferCNN):
    def __init__(self, topic_model_path, topic_word_dict_path):
        super(Sentiment, self).__init__(topic_model_path, topic_word_dict_path)
        self.name = 'sentiment_classify'

    def get_sentiment_prob(self, text):
        probs = self.infer(text)
        probs_dict = dict((idx, prob) for idx, prob in enumerate(probs))
        return probs_dict

    def get_sentiment(self, pos_prob, neg_prob):
        """
        Get sentiment score
        :param pos_prob:
        :param neg_prob:
        :return: 表示情感极性分类结果，0:负向，1:中性，2:正向
        """
        if pos_prob > neg_prob + 0.1:
            sentiment = 2
        elif neg_prob > pos_prob + 0.1:
            sentiment = 0
        else:
            sentiment = 1
        return sentiment

    def get_sentiment_confidence(self, pos_prob, neg_prob, sentiment):
        if sentiment == 0:
            confidence = pos_prob / 0.4
        elif sentiment == 1:
            confidence = np.abs(pos_prob - 0.5) / 0.1
        else:
            confidence = (pos_prob - 0.6) / 0.4
        return confidence

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
        sentiment = self.get_sentiment(pos_prob, neg_prob)
        items = dict()
        items["positive_prob"] = pos_prob
        items["negative_prob"] = neg_prob
        items['sentiment'] = sentiment
        items['confidence'] = self.get_sentiment_confidence(pos_prob, neg_prob, sentiment)
        result_dict['items'] = [items]
        return result_dict
