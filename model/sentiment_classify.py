# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from model.keras_model.infer import InferCNN
from util.io_util import get_logger

default_logger = get_logger(__file__)


class Sentiment(InferCNN):
    def __init__(self, model_path, word_dict_path, maxlen=300):
        super(Sentiment, self).__init__(model_path, word_dict_path, maxlen=maxlen)
        self.name = 'sentiment_classify'

    def get_sentiment_prob(self, text):
        probs = self.infer(text)
        probs_dict = dict((idx, prob) for idx, prob in enumerate(probs))
        return probs_dict

    def get_sentiment_confidence(self, pos_prob, pos_threshold=0.65, neg_threshold=0.45):
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
