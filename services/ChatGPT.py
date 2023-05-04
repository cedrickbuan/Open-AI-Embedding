import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import get_embedding, cosine_similarity

FILE_PATH = os.path.abspath(os.getcwd())
with open(FILE_PATH + '\openaiapikey.txt', 'r') as infile:  # get api key from text file
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


class ChatGPT():
    def __init__(self):
        self.model_engine = ""
        self.prompt = ""
        # Load our embeddings
        self.gunQAembeddings = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                        '../data/new_gun_data_embeddings.csv'))
        self.gunQAembeddings["embedding"] = self.gunQAembeddings.embedding.apply(
            eval).apply(np.array)
        self.initialMessage = f"""You are PBDionisio's chatbot. Answer the following question using only the context below. Always give the product link. If you don't know the answer for certain then suggest to browse our products here: https://www.pbdionisio.com/shop/
        
        \nContext: PBDionisio is a company opened monday to saturday starting 8am-5pm, located at 27 Don A. Roces Ave, Diliman, Quezon City, 1103 Metro Manila. 
        
        """

        self.messages = [
            {"role": "system", "content": self.initialMessage}
        ]

    def create_vector(self, text):  # convert text to vector representation
        return get_embedding(text, engine="text-embedding-ada-002")

    def search_in_question_and_answer_context(self, question):
        question_vector = self.create_vector(question)
        # find semilarities from the gun data vector column
        self.gunQAembeddings["similarities"] = self.gunQAembeddings['embedding'].apply(
            lambda x: cosine_similarity(x, question_vector))
        # get the first 4 matches only and combine them into one
        sortedResult = self.gunQAembeddings.sort_values(
            "similarities", ascending=False).head(4)
        context = []
        for i, row in sortedResult.iterrows():
            context.append(row['context'])
        return "\n".join(context)

    def update_chat(self, message, role, content):
        message.append({"role": role, "content": content})
        return message

    def get_chat_messages(self):
        return self.messages

    def ask_chatgpt_question(self, userQuestion):

        # add the result of the embedding to the context that will be the bases of the openai answer
        context = self.search_in_question_and_answer_context(userQuestion)
        self.messages = self.update_chat(
            self.messages, "system", "Add this to the context: " + context)
        # add the user question to the messages
        self.messages = self.update_chat(self.messages, "user", userQuestion)

        # get response from openai based on the context and question above
        # lets not add the max token for now. we will get an error about the max token the model can handle
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.2,
                top_p=1,
                frequency_penalty=0
            )

            self.messages = self.update_chat(self.messages, "assistant",
                                             response['choices'][0]['message']['content'])

        except Exception as e:
            return e

        return response['choices'][0]['message']['content']

    def check_if_text_is_positive(self, text):
        messages = [
            {"role": "system", "content": "determine if the TEXT below is positive or negative. Always say TRUE if text is positive and FALSE if text is negative. Always give explanation."},
            {"role": "user", "content": "TEXT: " + text}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2,
                top_p=1,
                frequency_penalty=0
            )
        except Exception as e:
            return str(e)
        return response['choices'][0]['message']['content']

    def check_if_image_is_positive(self, imageUrl):
        messages = [
            {"role": "system", "content": "determine if the IMAGE below is positive or negative. Return TRUE if image is positive and FALSE if image is negative. Always give explanation."},
            {"role": "user", "content": "IMAGE: " + imageUrl}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2,
                top_p=1,
                frequency_penalty=0
            )
        except Exception as e:
            return str(e)
        return response['choices'][0]['message']['content']
