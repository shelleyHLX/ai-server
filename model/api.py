# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from model import lexer, lm, word_emb

import config


class API(object):
    def __init__(self, model_type='lexer'):
        self.model_type = model_type
        if model_type == 'lexer':
            # 1. initialize model once and for all
            self.model = lexer.Lexer(custom_dict_path=config.custom_dict_path)
        elif model_type == 'lm':
            self.model = lm.LM(language_model_path=config.language_model_path)
        elif model_type == 'wordemb':
            self.model = word_emb.WordEmb(emb_path=config.emb_path)

    def generate_output_data(self, input_data=''):
        out = ''
        check_ret = self.model.check(input_data)
        if self.model_type == 'lexer':
            if check_ret:
                print(check_ret)
                items = check_ret['items']
                for item in items:
                    out += item['item'] + '/' + item['pos'] + ' '
        elif self.model_type == 'lm':
            if check_ret:
                print(check_ret)
                out = 'ppl: ' + str(check_ret['ppl'])
        elif self.model_type == 'wordemb':
            if check_ret:
                print(check_ret)
                out = 'vec: ' + str(check_ret['vec'])
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

        # 3. call model predict function
        out = self.generate_output_data(input_data)

        # 4. process the output
        output_data = {"input": input_data, "output": out}

        # 5. return the output for the api
        return output_data
