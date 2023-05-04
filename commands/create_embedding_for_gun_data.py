import openai
import pandas as pd
import os
from getpass import getpass
from openai.embeddings_utils import get_embedding

FILE_PATH = os.path.abspath(os.getcwd())
with open(FILE_PATH + '\openaiapikey.txt', 'r') as infile:  # get api key from text file
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                 '../data/new_gun_data_for_embedding.csv'))
print(df)
df['embedding'] = df['context'].apply(
    lambda x: get_embedding(x, engine='text-embedding-ada-002'))
df.to_csv(os.path.join(os.path.dirname(__file__),
          '../data/new_gun_data_embeddings.csv'))
