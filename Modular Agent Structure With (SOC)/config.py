# This file is just for the httpx client and api 

import httpx
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

client = httpx.Client(
    base_url ="https://generativelanguage.googleapis.com/v1beta",
    headers ={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    timeout=30
)

