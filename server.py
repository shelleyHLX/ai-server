# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
import sys
import logging
from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
from app.nlp_controller import NlpController

# define the app
app = Flask(__name__)
CORS(app)  # needed for cross-domain requests, allow everything by default

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
api_key = None


@app.route('/')
@app.route('/index')
def index():
    # return redirect(url_for('index'))
    return "Index API"


# API route
@app.route('/lexer_api', methods=['POST'])
def lexer_api():
    input_data = request.json
    app.logger.info("api_input: " + input_data)
    controller = NlpController(model_type='lexer', require_auth=False)
    output_data = controller.output(input_data)
    app.logger.info("api_output: " + output_data['input'] + '\t' + output_data['output'])
    return jsonify(output_data)


# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='127.0.0.1', port=5001, debug=True)
