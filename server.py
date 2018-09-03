# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
from flask import Flask, request, jsonify
from flask_cors import CORS

from app.controller import Controller
from config import ModelType
from utils.io_util import get_logger

default_logger = get_logger(__file__)
# define the app
app = Flask(__name__)
CORS(app)  # needed for cross-domain requests, allow everything by default

api_key = None


def process_request_json(input_data, model_type=ModelType.lexer_api):
    default_logger.info("api_input: " + input_data)
    controller = Controller(model_type=model_type, require_auth=False)
    output_data = controller.output(input_data)
    default_logger.info("api_output: " + output_data['output'])
    return jsonify(output_data)


@app.route('/')
@app.route('/index')
def index():
    # return redirect(url_for('index'))
    return "Index API"


# API route
@app.route('/lexer_api', methods=['POST'])
def lexer_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.lexer_api)


@app.route('/lm_api', methods=['POST'])
def lm_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.lm_api)


@app.route('/word_emb_api', methods=['POST'])
def word_emb_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.word_emb_api)


@app.route('/word_emb_sim_api', methods=['POST'])
def word_emb_sim_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.word_emb_sim_api)


@app.route('/short_text_sim_api', methods=['POST'])
def short_text_sim_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.short_text_sim_api)


@app.route('/keyword_api', methods=['POST'])
def keyword_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.keyword_api)


@app.route('/topic_api', methods=['POST'])
def topic_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.topic_api)


@app.route('/sentiment_classify_api', methods=['POST'])
def sentiment_classify_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.sentiment_classify_api)


@app.route('/corrector_api', methods=['POST'])
def corrector_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.corrector_api)


@app.route('/tts_api', methods=['POST'])
def tts_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.tts_api)


@app.route('/speech_recognition_api', methods=['POST'])
def speech_recognition_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.speech_recognition_api)


@app.route('/ocr_basic_api', methods=['POST'])
def ocr_basic_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.ocr_basic_api)


@app.route('/image_prediction_api', methods=['POST'])
def image_prediction_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.image_prediction_api)


@app.route('/image_detection_api', methods=['POST'])
def image_detection_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.image_detection_api)


@app.route('/image_quality_api', methods=['POST'])
def image_quality_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.image_quality_api)


@app.route('/image_repair_api', methods=['POST'])
def image_repair_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.image_repair_api)


@app.route('/image_compare_api', methods=['POST'])
def image_compare_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.image_compare_api)


@app.route('/colorize_api', methods=['POST'])
def colorize_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.colorize_api)


@app.route('/compose_api', methods=['POST'])
def compare_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.compose_api)


@app.route('/face_makeup_api', methods=['POST'])
def face_makeup_api():
    input_data = request.json
    return process_request_json(input_data, ModelType.face_makeup_api)


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
