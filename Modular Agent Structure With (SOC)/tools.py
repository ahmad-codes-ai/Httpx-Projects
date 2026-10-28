# This file is for python functions and tool registery

import random 
import httpx
from user_api import call_api


def get_random_number(max_num):
    result = random.randint(0,max_num)

    return {'result':result}


def get_weather(longitude,latitude):
    
    par = {
        'latitude':latitude,
        'longitude':longitude,
        'current' : 'temperature_2m,relative_humidity_2m,wind_speed_10m'
    }

    client = httpx.Client(
    base_url='https://api.open-meteo.com',
    params=par
    )

    response = call_api(client,'get','/v1/forecast')

    if response['ok'] is False:
        return response


    data = response['data']

    d = {
        'longitude': data.get('longitude'),
        'latitude': data.get('latitude'),
        'current_units': data.get('current_units'),
        'current': data.get('current')
    }


    return d 



registery = {

    # Tool 1
    'get_weather': {
        'function': get_weather,
        'schema': {
            'name': 'get_weather',
            'description': 'A Function to get weather of a place by providing its longitude and latitude',
            'parameters': {
                'type': 'OBJECT',
                'properties': {
                    'longitude': {
                        'type': 'NUMBER',
                        'description': 'The longitude of the place'
                    },
                    'latitude': {
                        'type': 'NUMBER',
                        'description': 'The latitude of the place'
                    },
                },
                'required': ['longitude','latitude']
            }
        }
    },


    # Tool 2
    'get_random_number': {
        "function": get_random_number,
        "schema": {
            "name": "get_random_number",
            "description": "Generates a random number between 0 and the provided maximum number.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "max_num": {"type": "INTEGER", "description": "The maximum number."}
                },
                "required": ["max_num"]
            }
        }
    }
    }
