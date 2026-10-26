import os 
import httpx
from user_api import *
from dotenv import load_dotenv
from safe_get import safe_get

load_dotenv()


token = os.getenv('GEMINI_API_KEY')




client = httpx.Client(

    base_url="https://generativelanguage.googleapis.com/v1beta",

    headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": token
    },

    timeout=30
)


history = []



print("Enter quit for exit")


while True:

    user = input("You: ")

    if user.lower() == 'quit':
        break

    du = {
        'role' : 'user',
        'parts': [{"text": user}]
    }

    history.append(du)




    payload = {
        'contents': history
    }

    response = call_api(client,'post','/models/gemini-3.5-flash-lite:generateContent',json=payload)

    if response['ok']:
        data = response['data']
        ai_text = safe_get(data,'candidates',0,'content','parts',0,'text')

        if ai_text is None:
            print("Gemini blocked the response or returned no text.")
            history.pop() # Remove the user message previous so dont mess up 
            continue

        print(f'Gemini: {ai_text}')
        print()

        dm = {
            'role' : 'model',
            'parts': [{"text": ai_text}]
        }

        history.append(dm)

    else:
        print('Something went wrong')

