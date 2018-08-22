# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
from flask import Flask, request, jsonify
from flask_cors import CORS

from app.nlp_controller import NlpController
from util.io_util import get_logger

default_logger = get_logger(__file__)
# define the app
app = Flask(__name__)
CORS(app)  # needed for cross-domain requests, allow everything by default

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
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='lexer', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/lm_api', methods=['POST'])
def lm_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='lm', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/wordemb_api', methods=['POST'])
def wordemb_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='wordemb', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/wordembsim_api', methods=['POST'])
def wordembsim_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='wordembsim', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/shorttextsim_api', methods=['POST'])
def shorttextsim_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='shorttextsim', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/keyword_api', methods=['POST'])
def keyword_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='keyword', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/topic_api', methods=['POST'])
def topic_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='topic', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/sentimentclassify_api', methods=['POST'])
def sentimentclassify_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='sentimentclassify', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/corrector_api', methods=['POST'])
def corrector_api():
    input_data = request.json
    default_logger.info("api_input: " + input_data)
    controller = NlpController(model_type='corrector', require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
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
