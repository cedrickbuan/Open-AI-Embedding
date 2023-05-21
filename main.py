from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pprint
from flask_cors import CORS
from services.ChatGPT import ChatGPT
from shared.Constant import Constant
from shared.Utils import Utils

app = Flask(__name__)
cors = CORS(app)  # all api calls below will be CORS ready
app.config['CORS_HEADERS'] = 'Content-Type'
chatgpt = ChatGPT()
CONSTANTS = Constant
UTILS = Utils
pp = pprint.PrettyPrinter(indent=4)

###############################
### Chat GPT api request    ###
###############################


@app.route(CONSTANTS.URLS['CHATGPT_QUESTION'], methods=['GET'])
def get():
    return chatgpt.get_chat_messages()


@app.route(CONSTANTS.URLS['CHATGPT_QUESTION'], methods=['POST'])
def askQuestion():
    response = chatgpt.ask_chatgpt_question(request.json['question'])
    return jsonify({'question': request.json['question'], 'gptanswer': response})


@app.route(CONSTANTS.URLS['CHATGPT_IS_TEXT_POSITIVE'], methods=['POST'])
def checkIfPositiveText():
    response = chatgpt.check_if_text_is_positive(request.json['message'])
    return jsonify({'isPositive': UTILS.checkIfHasPositive(response), 'gptanswer': response})


@app.route(CONSTANTS.URLS['CHATGPT_IS_IMAGE_POSITIVE'], methods=['POST'])
def checkIfPositiveImage():
    response = chatgpt.check_if_image_is_positive(request.json['image_url'])
    return jsonify({'isPositive': UTILS.checkIfHasPositive(response), 'gptanswer': response})


@app.route(CONSTANTS.URLS['CHATGPT_ADVICE'], methods=['POST'])
def getAdviceFromAi():
    response = chatgpt.get_ai_advice(request.json['question'])
    return jsonify({'gptanswer': response})

###############################
### END chat gpt request    ###
###############################


if __name__ == '__main__':
    app.run()
