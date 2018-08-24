# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: configuration

# api key
secret_key = [
    'secret_key'
]
# custom dict for segment
custom_dict_path = './data/custom_words.txt'

# kenlm language model
language_model_path = './data/people_chars_lm.klm'

# word embedding file path
emb_path = './data/sentence_w2v.bin'

# topic model
topic_model_path = './data/mcnn_model.h5'
topic_word_dict_path = './data/mcnn_vocab.txt'

# sentiment classify model
sentiment_model_path = './data/sentiment_hotel_model.h5'
sentiment_word_dict_path = './data/sentiment_hotel_vocab.txt'

# image
image_prediction = './data/resnet50_prediction.h5'
image_detection = './data/resnet50_detection.h5'
