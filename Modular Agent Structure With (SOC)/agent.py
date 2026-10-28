# The Agent Class and all memory / history / execution 


from user_api import call_api
from config import client
from tools import registery
from safe_get import safe_get



class Agent():

    def __init__(self):
        self.history = []
        self.system_instruction = {
            "parts": [{"text": "You are an ai assistant Use tools when needed only when user says or need Keep the converstaion short 2-4 lines max"}]
        }

    def run(self,text):

        du = {'role':'user','parts':[{'text':text}]}
        self.history.append(du) # Save the user message to the history
        
        while True:
  
            tools_schema = [tool['schema'] for tool in registery.values()]
            

            payload = {
                'tools': [{"function_declarations": tools_schema}],
                'contents': self.history,
                'systemInstruction': self.system_instruction
            }

            response = call_api(client,'POST','/models/gemini-3.5-flash-lite:generateContent',json=payload)

            if not response['ok']:
                print("Something went wrong")
                print(response)
                self.history.pop()
                break 

            data = response['data']
            parts = safe_get(data,'candidates',0,'content','parts')

            tool_responses = []

            for i in parts:

                if i.get('text'):
                    ai_text = i.get('text')
                    print(f'Gemini: {ai_text}\n')

                elif i.get('functionCall'):
                    call = i.get('functionCall')
                    name = call.get('name')
                    args = call.get('args')

                    if name in registery:
                        func = registery[name]['function']
                        result = func(**args)
                        d = {
                        "functionResponse": {
                        "name": name,
                        "response": result
                            }
                        }
                        tool_responses.append(d)
                        
                else:
                    print('The response dont have text/fucntion Call')

            dm = {'role':'model','parts':parts}
            self.history.append(dm)   # Saves the model response

            if tool_responses:
                self.history.append({'role':'user','parts':tool_responses})
                continue
            else:     # If no tool response means the model replied in text only one ended convo
                break



                



