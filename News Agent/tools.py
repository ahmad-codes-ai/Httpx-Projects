from config import * 
from user_api import *
from safe_get import safe_get
import httpx



def search_google(text):
   response = call_api(ser_client,'GET','',params={'q':text,'engine':'google','api_key':Ser_Api})

   if response['ok']:
      result = response.get('data').get('organic_results')
      return {'result':result}
   else:
      return {'error':response}


