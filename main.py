import requests
from dotenv import load_dotenv
import os

response = requests.get("")
load_dotenv()

my_python_key = os.getenv('API_KEY')