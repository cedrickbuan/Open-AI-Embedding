import openai
import pprint
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

# Load our embeddings
gunQAembeddings = pd.read_csv(os.path.join(os.path.dirname(
    __file__), '../data/new_gun_data_embeddings.csv'))
gunQAembeddings["embedding"] = gunQAembeddings.embedding.apply(
    eval).apply(np.array)

pp = pprint.PrettyPrinter(indent=4)


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

pp.pprint(messages)


if __name__ == '__main__':
    while True:
        user = input('\nUser:\n')

        # add the result of the embedding to the context that will be the bases of the openai answer
        context = search_in_question_and_answer_context(user)
        messages = update_chat(
            messages, "system", "Add this to the context: " + context)
        # add the user question to the messages
        messages = update_chat(messages, "user", user)

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

        pp.pprint(messages)


# SAMPLE response

# [   {   'content': "You are PBDionisio's chatbot. Answer the following "
#                    'question using only the context below. Always give the '
#                    "product link. If you don't know the answer for certain "
#                    'then suggest to browse our products here: '
#                    'https://www.pbdionisio.com/shop/\n'
#                    '        \n'
#                    '        \n'
#                    'Context: PBDionisio is a company opened monday to saturday '
#                    'starting 8am-5pm, located at 27 Don A. Roces Ave, Diliman, '
#                    'Quezon City, 1103 Metro Manila. \n'
#                    '        \n'
#                    '        ',
#         'role': 'system'},
#     {'content': '', 'role': 'user'},
#     {'content': '', 'role': 'assistant'},
#     {   'content': 'Add this to the context: Description for Inglis Hi-Power?. '
#                    'Manufacture date for Inglis Hi-Power?. How much is the '
#                    'Inglis Hi-Power?. Do you have Inglis Hi-Power?. The gun '
#                    'named Inglis Hi-Power is manufactured by John Inglis and '
#                    'Company and uses the 9\\u00d719mm Parabellum cartridge. '
#                    'Created from Canada and produced in the year 1943. The '
#                    'Inglis Hi-Power is wort 5723 dollars with a discount of '
#                    '30-40%. You can buy the Inglis Hi-Power using this link: '
#                    'https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/\n'
#                    'Description for Horhe (pistol)?. Manufacture date for '
#                    'Horhe (pistol)?. How much is the Horhe (pistol)?. Do you '
#                    'have Horhe (pistol)?. The gun named Horhe (pistol) is '
#                    'manufactured by Klimovsk Specialized Ammunition Plant and '
#                    'uses the 9 mm P.A. cartridge. Created from Russia and '
#                    'produced in the year 2006. The Horhe (pistol) is wort 4179 '
#                    'dollars with a discount of 30-40%. You can buy the Horhe '
#                    '(pistol) using this link: '
#                    'https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/\n'
#                    'Description for HS2000?. Manufacture date for HS2000?. How '
#                    'much is the HS2000?. Do you have HS2000?. The gun named '
#                    'HS2000 is manufactured by HS Produkt and uses the '
#                    '9\\u00d719mm Parabellum .357 SIG cartridge. Created from '
#                    'Croatia and produced in the year 1999. The HS2000 is wort '
#                    '356 dollars with a discount of 30-40%. You can buy the '
#                    'HS2000 using this link: '
#                    'https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/\n'
#                    'Description for Hi-Point C-9?. Manufacture date for '
#                    'Hi-Point C-9?. How much is the Hi-Point C-9?. Do you have '
#                    'Hi-Point C-9?. The gun named Hi-Point C-9 is manufactured '
#                    'by Hi-Point Firearms and uses the 9\\u00d719mm Parabellum '
#                    'cartridge. Created from United States and produced in the '
#                    'year 2010. The Hi-Point C-9 is wort 6966 dollars with a '
#                    'discount of 30-40%. You can buy the Hi-Point C-9 using '
#                    'this link: '
#                    'https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/',
#         'role': 'system'},
#     {'content': 'hi who are you? are you open today?', 'role': 'user'},
#     {   'content': "Hello! I am PBDionisio's chatbot. PBDionisio is a company "
#                    'located at 27 Don A. Roces Ave, Diliman, Quezon City, 1103 '
#                    'Metro Manila. We are open from Monday to Saturday starting '
#                    'at 8am-5pm. You can browse our products here: '
#                    'https://www.pbdionisio.com/shop/',
#         'role': 'assistant'}]
