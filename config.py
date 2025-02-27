import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 
openai_api_key = os.environ['OPENAI_API_KEY']
huggingface_api_key = os.environ['HUGGINGFACE_API_KEY']