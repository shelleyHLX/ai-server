# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from util.io_util import get_logger
from model.keras_model.infer import InferCNN
import operator

default_logger = get_logger(__file__)

label_revserv_dict = {0: '人类作者',
                      1: '机器作者',
                      2: '机器翻译',
                      3: '自动摘要'}


class Topic(InferCNN):
    def __init__(self, topic_model_path, topic_word_dict_path):
        super(Topic, self).__init__(topic_model_path, topic_word_dict_path)
        self.name = 'topic'

    def get_topic(self, text):
        topic_probs = self.infer(text)
        topic_probs_dict = dict((idx, prob) for idx, prob in enumerate(topic_probs))
        topic_probs_order_dict = sorted(topic_probs_dict.items(), key=operator.itemgetter(1), reverse=True)
        return topic_probs_order_dict

    def check(self, text):
        """
        Args:
            text: 欧洲冠军联赛是欧洲足球协会联盟主办的年度足球比赛
        Returns:
        {
            "log_id": 3591049593939822907,
            "item": {
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
