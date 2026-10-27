import httpx
import os 
from user_api import * 
from safe_get import safe_get
from dotenv import load_dotenv
import random


load_dotenv()


def get_random_number(max_num):
    if type(max_num) is int:
        result = random.randint(0,max_num)

        return {'result':result}
    else:
        return {'result':None}



token = os.getenv('GEMINI_API_KEY')

client = httpx.Client(
    base_url = "https://generativelanguage.googleapis.com/v1beta",
    headers = {
        'Content-type':'application/json',
        "x-goog-api-key": token,
    }
)


tools = [                                    # List of all tools (fucntions) provided to an AI
    {
        "function_declarations": [
            {
                "name": "get_random_number",
                "description": "Generates a random number between 0 and the provided maximum number.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {      # The parameters that are needed
                        "max_num": {
                            "type": "INTEGER",   # Could be a STRING too 
                            "description": "The maximum possible number."
                        }   # If another parameter exits come after this
                    },
                    "required": ["max_num"]    # Which parameteres are mandatory 
                }
            }  # If there exist another tool another dict will follow same pattern from here 
        ]
    }
]



print('Enter quit to exist')

history = []





while True:    # Outer loop for the input

    user_text = input("You: ")

    if user_text.lower().strip() == 'quit':
        break

    du = {
        'role':'user',
        'parts': [{"text": user_text}]
    }

    history.append(du)

    while True:   # Inner loop for calling a function multiple time 

        payload = {
            'contents' : history,     # This give all conversation so far too ai
            'tools' : tools,          # Providing the tool list
            "systemInstruction": {
            "parts": [{"text": "You are an ai assistant and keep your answers in 2-3 lines answering what the user asks use tools when needed."}]
            }, 
        }


        response = call_api(client,'POST','/models/gemini-3.5-flash-lite:generateContent',json=payload)



        if response['ok'] is True:
            data = response['data']
            ai_response = safe_get(data,'candidates',0,'content','parts')

            results = []     # results of all tool calls

            for i in ai_response:

                if i.get('text'):
                    ai_text = i.get('text')
                    print(f"Gemini: {ai_text}")
                    print()
                   

                elif i.get('functionCall'):
                    call = i.get('functionCall')

                    name = call.get('name')
                    args = call.get('args')

                    if name == 'get_random_number' and args.get('max_num'):
                        r = get_random_number(max_num = args.get('max_num'))
                        

                        d = {
                            "functionResponse": {
                            "name": name,
                            "response": r
                            }
                        }

                        results.append(d)

            history.append({'role': 'model', 'parts': ai_response})
            
            if results:

                history.append({'role':'model',
                                'parts':ai_response}
                                )

                history.append(
                    {'role':'user',
                     'parts': results}
                )

                continue

            else:
                break


                        
        else:
            print("Something went wrong")
            history.pop()   # Since the response is not generated remove the user message from history to avoid conflict later
            break



# Full agent with a tool call 

