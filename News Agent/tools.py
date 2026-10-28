from config import * 
from user_api import *
from safe_get import safe_get
import httpx
import os 



def search_google(text):
   response = call_api(ser_client,'GET','',params={'q':text,'engine':'google','api_key':Ser_Api})

   if response['ok']:
      result = response.get('data').get('organic_results')
      return {'result':result}
   else:
      return {'error':response}


def fetch_url(url):
    response = call_api(jina_client,'GET',f'/{url}')

    if response['ok']:
        data = response['data']['data']['content']
        return {'result':data}
    else:
       return {'result':response}
        


def save_to_file(file_name,text):
    try:
      with open(file_name,'w',encoding="utf-8") as f:
         f.write(text)
         return {'result':'Suceessfully write in file'}
    except:
      return {'result': 'Error occured'}



      
TOOL_REGISTRY = {
    'search_google': {
        'function': search_google,
        'schema': {
            'name': 'search_google',
            'description': 'A Function to search Google and return the organic search results for a given text query.They contain a title and the link to wesbites mainly',
            'parameters': {
                'type': 'OBJECT',
                'properties': {
                    'text': {
                        'type': 'STRING',
                        'description': 'The search query text to look up on Google.'
                    },
                },
                'required': ['text']
            }
        }
    },


    
    'fetch_url': {
        'function': fetch_url,
        'schema': {
            'name': 'fetch_url',
            'description': 'A Function to fetch the content of a web page by providing its url. It will give full content of that web page',
            'parameters': {
                'type': 'OBJECT',
                'properties': {
                    'url': {
                        'type': 'STRING',
                        'description': 'The full URL of the page to fetch.'
                    },
                },
                'required': ['url']
            }
        }
    },


    
    'save_to_file': {
        'function': save_to_file,
        'schema': {
            'name': 'save_to_file',
            'description': 'A Function to save the given text into a file with the specified file name.',
            'parameters': {
                'type': 'OBJECT',
                'properties': {
                    'file_name': {
                        'type': 'STRING',
                        'description': 'The name or path of the file to write to.You name this based on contents of file and it get created'
                    },
                    'text': {
                        'type': 'STRING',
                        'description': 'The text content to write into the file.Use the python string can include /n for new lines and t for tab spaces and all'
                    },
                },
                'required': ['file_name', 'text']
            }
        }
    }    
      
}