# The Agent Class and all memory / history / execution 


from user_api import call_api
from config import gemini_client
from tools import registery
from safe_get import safe_get



class Agent():

    def __init__(self):
        self.history = []
        self.system_instruction = {
            "parts": [{"text": "You are an ai assistant that tell user latest news and can also also normal questions but mainly you are a news agent Use tools when needed your flow for a news can look like this first user tell a topic you call the google serach tool with related query get the title and links of the webpages then the one you think is relevant you use the url fetcher tool to get the content of that webpage analyze and then do this 2-3 times like minimum you should send user news after checking and colecting key detailes from 2-3 web pages minimum if user says more you can go fro it and then after you have every info regarding user news you write to a file and in file you write html css code all in one so when user open that file in a web browser he see a beautifull interface use dark theme clean interface fluid proper use triple quotes to start and end for this bcz html itself has double quote thing so keep it in mind and file name you decide based on content beautifully present and should be 800 words min with proper web layout if user say more max limit is 1200 words. and all this is for the file while talking with user dont dump eveything there talk with him in 2-3 lines short and tell main news is saved at the file name you save ok with user talk simple short also in the webpage at end provide actual link of sources you used for the data"}]
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

            response = call_api(gemini_client,'POST','/models/gemini-3.5-flash-lite:generateContent',json=payload)

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
                        try:
                            func = registery[name]['function']
                            result = func(**args)
                            d = {
                            "functionResponse": {
                            "name": name,
                            "response": result
                                }
                            }
                            tool_responses.append(d)

                        except Exception as e:
                            d = {
                            "functionResponse": {
                            "name": name,
                            "response": {'error':f"This error occured {e}"}
                                }
                            }
                            tool_responses.append(d)
                            
                    else:
                        d = {
                        "functionResponse": {
                        "name": name,
                        "response": {'error':f'The tool {name} does not exist'}
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
