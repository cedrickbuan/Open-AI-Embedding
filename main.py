from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import openai
import pandas as pd
import numpy as np
import pprint
from openai.embeddings_utils import get_embedding, cosine_similarity
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

pp = pprint.PrettyPrinter(indent=4)

with open('openaiapikey.txt', 'r') as infile:  # get api key from text file
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

# Load our embeddings
gunQAembeddings = pd.read_csv('data/new_gun_data_embeddings.csv')
gunQAembeddings["embedding"] = gunQAembeddings.embedding.apply(
    eval).apply(np.array)


def create_vector(text):  # convert text to vector representation
    return get_embedding(text, engine="text-embedding-ada-002")


def search_in_question_and_answer_context(question):
    question_vector = create_vector(question)
    # find semilarities from the gun data vector column
    gunQAembeddings["similarities"] = gunQAembeddings['embedding'].apply(
        lambda x: cosine_similarity(x, question_vector))
    # get the first 4 matches only and combine them into one
    sortedResult = gunQAembeddings.sort_values(
        "similarities", ascending=False).head(4)
    context = []
    for i, row in sortedResult.iterrows():
        context.append(row['context'])
    return "\n".join(context)


def update_chat(message, role, content):
    message.append({"role": role, "content": content})
    return message


initialMessage = f"""You are PBDionisio's chatbot. Answer the following question using only the context below. Always give the product link. If you don't know the answer for certain then suggest to browse our products here: https://www.pbdionisio.com/shop/
        
        \nContext: PBDionisio is a company opened monday to saturday starting 8am-5pm, located at 27 Don A. Roces Ave, Diliman, Quezon City, 1103 Metro Manila. 
        
        """

messages = [
    {"role": "system", "content": initialMessage},
    {"role": "user", "content": ""},
    {"role": "assistant", "content": ""}

]


@app.route('/chatgpt/question', methods=['GET'])
def get():
    return jsonify(messages)


@app.route('/chatgpt/question', methods=['POST'])
def askQuestion():
    global messages
    userQuestion = request.json['question']

    # add the result of the embedding to the context that will be the bases of the openai answer
    context = search_in_question_and_answer_context(userQuestion)
    messages = update_chat(
        messages, "system", "Add this to the context: " + context)
    # add the user question to the messages
    messages = update_chat(messages, "user", userQuestion)

    # get response from openai based on the context and question above
    # lets not add the max token for now. we will get an error about the max token the model can handle
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        top_p=1,
        frequency_penalty=0
    )

    messages = update_chat(messages, "assistant",
                           response['choices'][0]['message']['content'])

    return jsonify({'question': request.json['question'], 'gptanswer': response['choices'][0]['message']['content']})


pp.pprint(messages)
if __name__ == '__main__':
    app.run()
