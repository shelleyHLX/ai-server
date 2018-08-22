# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

import config
from model import lexer, lm, word_emb, word_emb_sim, \
    short_text_sim, keyword, topic, sentiment_classify, corrector


class API(object):
    def __init__(self, model_type='lexer'):
        self.model_type = model_type
        self.lexer_model = lexer.Lexer.get_instance(custom_dict_path=config.custom_dict_path)
        self.lm_model = lm.LM.get_instance(language_model_path=config.language_model_path)
        self.word_emb_model = word_emb.WordEmb.get_instance(emb_path=config.emb_path)
        self.word_emb_sim_model = word_emb_sim.WordEmbSim.get_instance(emb_path=config.emb_path)
        self.short_text_sim_model = short_text_sim.ShortTextSim.get_instance(emb_path=config.emb_path)
        self.keyword_model = keyword.Keyword.get_instance()
        self.topic_model = topic.Topic.get_instance(config.topic_model_path, config.topic_word_dict_path)
        self.sentiment_model = sentiment_classify.Sentiment.get_instance(config.sentiment_model_path,
                                                                         config.sentiment_word_dict_path)
        self.corrector_model = corrector.Corrector()

    def generate_output_data(self, input_data=''):
        out = ''
        if self.model_type == 'lexer':
            check_ret = self.lexer_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['item'] + '/' + item['pos'] + ' '
        elif self.model_type == 'lm':
            check_ret = self.lm_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'ppl: ' + str(check_ret['ppl'])
        elif self.model_type == 'wordemb':
            check_ret = self.word_emb_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'vec: ' + str(check_ret['vec'])
        elif self.model_type == 'wordembsim':
            check_ret = self.word_emb_sim_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'score: ' + str(check_ret['score'])
        elif self.model_type == 'shorttextsim':
            check_ret = self.short_text_sim_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'score: ' + str(check_ret['score'])
        elif self.model_type == 'keyword':
            check_ret = self.keyword_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['tag'] + ' '
        elif self.model_type == 'topic':
            check_ret = self.topic_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out += item['tag'] + '/' + str(item['score']) + ' '
        elif self.model_type == 'sentimentclassify':
            check_ret = self.sentiment_model.check(input_data)
            print(check_ret)
            if check_ret:
                items = check_ret['items']
                for item in items:
                    out = 'sentiment:' + str(item['sentiment']) + ' positive_prob:' + \
                          str(item['positive_prob']) + ' negative_prob:' + str(item['negative_prob'])
        elif self.model_type == 'corrector':
            check_ret = self.corrector_model.check(input_data)
            print(check_ret)
            if check_ret:
                out = 'corrected_text:' + str(check_ret['corrected_text'])
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
