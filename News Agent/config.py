import os 
from dotenv import load_dotenv
import httpx

load_dotenv()


Gemini_Api = os.getenv('GEMINI_API_KEY')
Ser_Api = os.getenv('SER_API_KEY')
Jina_Api = os.getenv('JINA_API_KEY')

gemini_client = httpx.Client(
    base_url ="https://generativelanguage.googleapis.com/v1beta",
    headers ={
        "Content-Type": "application/json",
        "x-goog-api-key": Gemini_Api
    },
    timeout=60
)


ser_client = httpx.Client(
    base_url = 'https://serpapi.com/search.json',
    headers = {
        'Content-Type': "apllication/json",
    },
    timeout=60
)

jina_client = httpx.Client(
    base_url = "https://r.jina.ai",
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {Jina_Api}",
    },
    timeout = 60
)




