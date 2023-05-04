import openai
import pandas as pd
import os
from getpass import getpass
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                 '../data/new_gun_data_for_embedding.csv'))
print(df)
df['embedding'] = df['context'].apply(
    lambda x: get_embedding(x, engine='text-embedding-ada-002'))
df.to_csv(os.path.join(os.path.dirname(__file__),
          '../data/new_gun_data_embeddings.csv'))
