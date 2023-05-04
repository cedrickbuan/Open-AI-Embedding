from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pprint
from flask_cors import CORS
from services.ChatGPT import ChatGPT
from shared.Constant import Constant

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
chatgpt = ChatGPT()
CONSTANTS = Constant
pp = pprint.PrettyPrinter(indent=4)


@app.route(CONSTANTS.URLS['CHATGPT_QUESTION'], methods=['GET'])
def get():
    return chatgpt.get_chat_messages()


@app.route(CONSTANTS.URLS['CHATGPT_QUESTION'], methods=['POST'])
def askQuestion():
    response = chatgpt.ask_chatgpt_question(request.json['question'])
    return jsonify({'question': request.json['question'], 'gptanswer': response})


if __name__ == '__main__':
    app.run()
