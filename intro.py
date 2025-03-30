import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv

# https://deployai.streamlit.app/

'''
if load_dotenv():
    df = pd.read_csv('Titanic.csv')

    sdf = SmartDataframe(df)

    response = sdf.chat('Make a pie chart people survived by gender')
    print(response)
'''
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_token=api_key)

if not api_key:
    raise ValueError("Missing OPENAI API KEY")

df = pd.read_csv('Titanic.csv')

# Create SmartDataFrame with LLM
sdf = SmartDataframe(df, config={"llm": llm})

response = sdf.chat('Make a pie chart people survived by gender')
print(response)