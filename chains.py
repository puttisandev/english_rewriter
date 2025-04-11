from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from prompts import prompt_template
import os
from config import OPENAI_API_KEY

def build_chain(style="default"):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    parser = StrOutputParser()
    return prompt_template | model | parser