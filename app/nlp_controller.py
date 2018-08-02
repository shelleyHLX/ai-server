# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

from config import secret_key
from model.api import API


class NlpController(object):
    def __init__(self, model_type='lexer', max_sentence_len=250, require_auth=True):
        self.max_sentence_len = max_sentence_len
        self.require_auth = require_auth
        self.model_type = model_type

    def authenticate(self, api_key=None):
        if not self.require_auth:
            pass
        else:
            if not api_key: raise self.errors.append("missing api_key")
            print('checking key')
            if not (api_key in secret_key):
                print('not in list')
                raise self.errors.append("invalid api key")
            pass

    def output(self, input_data='', api_key=None):
        output_data = ''
        try:
            self.authenticate(api_key)
            model_api = API(self.model_type)
            output_data = model_api.get_model_output(input_data=input_data)
        except Exception as e:
            print(e, 'error')
        return output_data
