# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 

from model import lexer
import config


class API(object):
    def __init__(self, model_type='lexer'):
        self.model_type = model_type
        if self.model_type == 'lexer':
            # 1. initialize model once and for all
            self.model = lexer.Lexer(custom_dict_path=config.custom_dict_path)
            print(self.model.check('i am a little one'))
        elif model_type == 'kenlm':
            pass

    def generate_output_data(self, input_data=''):
        out = ''
        if self.model_type == 'lexer':
            check_ret = self.model.check(input_data)
            if check_ret:
                print(check_ret)
                items = check_ret['items']
                for item in items:
                    out += item['item'] + '/' + item['pos'] + ' '
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
