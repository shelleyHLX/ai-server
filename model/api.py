# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: api for model

import config
from config import ModelType
from model.image import ocr, colorize, compose, detection, face_makeup, \
    prediction, quality_audit, repair, compare
from model.nlp import corrector, sentiment_classify, short_text_sim, \
    keyword, lm, word_emb_sim, topic, word_emb, lexer
from model.speech import text_to_speech, speech_recognition


class API(object):
    def __init__(self, model_type='lexer'):
        self.model_type = model_type
        # nlp
        self.lexer_model = lexer.Lexer.get_instance(custom_dict_path=config.custom_dict_path)
        self.lm_model = lm.LM.get_instance(language_model_path=config.language_model_path)
        self.word_emb_model = word_emb.WordEmb.get_instance(emb_path=config.emb_path)
        self.word_emb_sim_model = word_emb_sim.WordEmbSim.get_instance(emb_path=config.emb_path)
        self.short_text_sim_model = short_text_sim.ShortTextSim.get_instance(emb_path=config.emb_path)
        self.keyword_model = keyword.Keyword.get_instance()
        self.topic_model = topic.Topic.get_instance(config.topic_model_path, config.topic_word_dict_path)
        self.sentiment_model = sentiment_classify.Sentiment.get_instance(config.sentiment_model_path,
                                                                         config.sentiment_word_dict_path)
        self.corrector_model = corrector.Corrector.get_instance()
        # speech
        self.tts_model = text_to_speech.TextToSpeech.get_instance(model_path=config.syllables_dir)
        self.speech_recognition_model = speech_recognition.SpeechRecognition.get_instance()
        # image
        self.ocr_basic_model = ocr.Ocr.get_instance()
        self.image_prediction_model = prediction.Prediction.get_instance(model_path=config.image_prediction)
        self.image_detection_model = detection.Detection.get_instance(model_path=config.image_detection)
        self.image_repair_model = repair.Repair.get_instance()
        self.image_quality_model = quality_audit.QualityAduit.get_instance()
        self.image_compare_model = compare.Compare.get_instance()
        self.colorize_model = colorize.Colorize.get_instance(model_path=config.colorize_model_path)
        self.compose_model = compose.Compose.get_instance(model_path=config.compose_model_path,
                                                          compose_image_path=config.compose_image_path)
        self.face_makeup_model = face_makeup.FaceMakeup.get_instance()

    def generate_output_data(self, input_data=''):
        out = ''
        if self.model_type == ModelType.lexer_api:
            check_ret = self.lexer_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['item'] + '/' + item['pos'] + ' '
        elif self.model_type == ModelType.lm_api:
            check_ret = self.lm_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'ppl: ' + str(check_ret['ppl'])
        elif self.model_type == ModelType.word_emb_api:
            check_ret = self.word_emb_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'vec: ' + str(check_ret['vec'])
        elif self.model_type == ModelType.word_emb_api:
            check_ret = self.word_emb_sim_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'score: ' + str(check_ret['score'])
        elif self.model_type == ModelType.short_text_sim_api:
            check_ret = self.short_text_sim_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'score: ' + str(check_ret['score'])
        elif self.model_type == ModelType.keyword_api:
            check_ret = self.keyword_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['tag'] + ' '
        elif self.model_type == ModelType.word_emb_api:
            check_ret = self.topic_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['tag'] + '/' + str(item['score']) + ' '
        elif self.model_type == ModelType.sentiment_classify_api:
            check_ret = self.sentiment_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out = 'sentiment:' + str(item['sentiment']) + ' positive_prob:' + \
                          str(item['positive_prob']) + ' negative_prob:' + str(item['negative_prob'])
        elif self.model_type == ModelType.corrector_api:
            check_ret = self.corrector_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'corrected text:' + str(check_ret['corrected_text'])
        elif self.model_type == ModelType.tts_api:
            check_ret = self.tts_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output_base64']
        elif self.model_type == ModelType.speech_recognition_api:
            check_ret = self.speech_recognition_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output']
        elif self.model_type == ModelType.ocr_basic_api:
            check_ret = self.ocr_basic_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output']
        elif self.model_type == ModelType.image_prediction_api:
            check_ret = self.image_prediction_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['name'] + '/' + str(item['score']) + ' '
        elif self.model_type == ModelType.image_detection_api:
            check_ret = self.image_detection_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['name'] + '/' + str(item['score']) + ' '
        elif self.model_type == ModelType.image_repair_api:
            check_ret = self.image_repair_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output_base64']
        elif self.model_type == ModelType.image_quality_api:
            check_ret = self.image_quality_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'clarity:' + str(check_ret['clarity']) + '\t' + check_ret['output']
        elif self.model_type == ModelType.image_compare_api:
            check_ret = self.image_compare_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'similarity score:' + check_ret['score']
        elif self.model_type == ModelType.colorize_api:
            check_ret = self.colorize_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output_base64']
        elif self.model_type == ModelType.compose_api:
            check_ret = self.compose_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output_base64']
        elif self.model_type == ModelType.face_makeup_api:
            check_ret = self.face_makeup_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = check_ret['output_base64']
        return out

    def get_model_output(self, input_data=''):
        """
        Args:
            input_data: submitted to the API, raw string
        Returns:
            output_data: after some transformation, to be
                returned to the API
        """
        # 2. process input
        input_data = input_data.strip()

        # 3. call lexer_model predict function
        out = self.generate_output_data(input_data)

        # 4. process the output
        output_data = {"input": input_data, "output": out}

        # 5. return the output for the api
        return output_data
