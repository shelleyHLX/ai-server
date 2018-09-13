# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: configuration

# api key
secret_key = [
    'secret_key'
]


# api parrots_model type
class ModelType(object):
    # nlp
    lexer_api = "lexer"
    lm_api = 'lm'
    word_emb_api = 'word_emb'
    word_emb_sim_api = 'word_emb_sim'
    short_text_sim_api = 'short_text_sim'
    keyword_api = 'keyword'
    topic_api = 'topic'
    sentiment_classify_api = 'sentiment_classify'
    corrector_api = 'corrector'
    # speech
    tts_api = 'tts'
    speech_recognition_api = 'speech_recognition'
    # image
    ocr_basic_api = 'ocr_basic'
    image_prediction_api = 'image_prediction'
    image_detection_api = 'image_detection'
    image_quality_api = 'image_quality'
    image_repair_api = 'image_repair'
    image_compare_api = 'image_compare'
    colorize_api = 'colorize'
    compose_api = 'compose'
    face_makeup_api = 'face_makeup'


# -------------- NLP --------------#
# custom dict for segment
custom_dict_path = './data/custom_words.txt'

# kenlm language parrots_model
language_model_path = './data/people_chars_lm.klm'

# word embedding file path
emb_path = './data/sentence_w2v.bin'

# topic parrots_model
topic_model_path = './data/mcnn_model.h5'
topic_word_dict_path = './data/mcnn_vocab.txt'

# sentiment classify parrots_model
sentiment_model_path = './data/sentiment_hotel_model.h5'
sentiment_word_dict_path = './data/sentiment_hotel_vocab.txt'

# -------------- Image --------------#
# image prediction
image_prediction = './data/resnet50_prediction.h5'

# image detection
image_detection = './data/resnet50_detection.h5'

# image colorize
train_input_image_path = './data/images/colorize_train.png'
colorize_model_path = './data/cartoon_colorize.h5'

# image compose
compose_model_path = './data/haarcascade_frontalface_default.xml'
compose_image_path = './data/images/hat_compose.png'

# -------------- Speech --------------#
# text to speech
syllables_dir = './data/syllables'
