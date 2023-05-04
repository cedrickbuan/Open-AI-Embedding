import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

# Load our embeddings
gunQAembeddings = pd.read_csv('../data/new_gun_data_embeddings.csv')
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


if __name__ == '__main__':
    while True:
        user = input('\nUser:\n')
        context = search_in_question_and_answer_context(user)
        # gives openai the initial data for our company and how should it behave when answering
        prompt = f"""You are PBDionisio's chatbot. PBDionisio is a company opened monday to saturday starting 8am-5pm, located at 27 Don A. Roces Ave, Diliman, Quezon City, 1103 Metro Manila. Answer the following question using only the context below. Always give the product link. If you don't know the answer for certain then suggest to browse our products here: https://www.pbdionisio.com/shop/. 
        
        \nContext: {context}.
        

        \n{user}\n.


        """
        # print(prompt)
        response = openai.Completion.create(
            engine=os.environ['COMPLETION_MODEL'],
            prompt=prompt,
            max_tokens=500,
            temperature=0.2,
            top_p=1,
            frequency_penalty=0
        )

        print("ChatBot: " + response['choices'][0]['text'])


# SAMPLE CHAT RESULT
# User:
# where are you located?
# ChatBot: We are located at 27 Don A. Roces Ave, Diliman, Quezon City, 1103 Metro Manila.

# User:
# are you open today?
# ChatBot:
# Yes, we are open today from 8am to 5pm. You can browse our products here: https://www.pbdionisio.com/shop/

# User:
# do you have a beretta 9000?
# ChatBot: Yes, we do have the Beretta 9000. You can buy it using this link: https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/.

# User:
# how much is the beretta 9000?
# ChatBot:
# The Beretta 9000 is wort 6128 dollars with a discount of 30-40%. You can buy the Beretta 9000 using this link: https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/
