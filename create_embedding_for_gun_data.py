import openai
import pandas as pd
import numpy as np
from getpass import getpass
from openai.embeddings_utils import get_embedding

with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

df = pd.read_csv('data/new_gun_data_for_embedding.csv')
print(df)
df['embedding'] = df['context'].apply(
    lambda x: get_embedding(x, engine='text-embedding-ada-002'))
df.to_csv('data/new_gun_data_embeddings.csv')
