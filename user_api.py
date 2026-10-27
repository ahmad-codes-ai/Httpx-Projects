import re
import httpx
import time
import random


# Dont delete this file


def extract(pattern,header):

    if not header:
        return None   # safety check
    
    match = re.search(pattern, header)  #github link <([^>]+)>;\s*rel="next"
    return match.group(1) if match else None



def make_result(ok=False,status=None,data=None,reason=None,headers=None):

    return {
        'ok':ok,
        'status':status,
        'data':data,
        'reason':reason,
        'headers': headers
    }



def parse_status(response):   # Found online have almost all specific erros that can come 
    code = response.status_code

    # ─── 2xx Success ──────────────────────────────
    if 200 <= code < 300:
        return None

    # ─── 4xx Client errors (specific) ─────────────
    if code == 400: return "bad_request"
    if code == 401: return "unauthorized"
    if code == 402: return "payment_required"
    if code == 403: return "forbidden"
    if code == 404: return "not_found"
    if code == 405: return "method_not_allowed"
    if code == 406: return "not_acceptable"
    if code == 408: return "request_timeout"
    if code == 409: return "conflict"
    if code == 410: return "gone"
    if code == 413: return "payload_too_large"
    if code == 415: return "unsupported_media_type"
    if code == 422: return "invalid_data"
    if code == 429: return "rate_limit"

    # ─── 5xx Server errors (specific) ─────────────
    if code == 500: return "server_error"
    if code == 501: return "not_implemented"
    if code == 502: return "bad_gateway"
    if code == 503: return "service_unavailable"
    if code == 504: return "gateway_timeout"

    # ─── Family fallbacks ─────────────────────────
    if 400 <= code < 500: return "client_error"
    if 500 <= code < 600: return "server_error"
    if 300 <= code < 400: return "redirect"
    if 100 <= code < 200: return "informational"

    return "unknown_status"

def jittered(seconds):
    return seconds + random.uniform(0,seconds*0.5)


IDEMPOTENT_METHODS = {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}

def call_api(client,method,path,max_attempt=3,sleep=1,**kwargs):

    is_idempotent = method.upper() in IDEMPOTENT_METHODS

    for attempt in range(max_attempt):

        try:
            response = client.request(method,path,**kwargs)


        except httpx.TimeoutException:

            if not is_idempotent:
                return make_result(reason='timeout')
            
            if attempt == max_attempt-1:
                return make_result(reason='timeout')

            time.sleep(jittered(sleep))  # else if both false
            sleep = sleep * 2
            continue


        except httpx.ConnectError:

            if not is_idempotent:
                return make_result(reason='network error')

            if attempt == max_attempt -1:
                return make_result(reason='network Error')

            time.sleep(jittered(sleep))
            sleep = sleep * 2
            continue


        if 500 <= response.status_code < 600:  # Server Side error in each

            if attempt == max_attempt - 1:
                return make_result(status=response.status_code,reason='Server Error')

            time.sleep(jittered(sleep))
            sleep = sleep * 2
            continue


        if response.status_code == 429:   # Rate Limit

            if attempt == max_attempt - 1:
                return make_result(status=response.status_code,reason='rate_limit')

            
            retry_after = response.headers.get('Retry-After')

            if retry_after and retry_after.isdigit():  # Imp to check isdigit to be sure its in seconds / can be a date too 
                wait = int(retry_after)
                time.sleep(wait)
                continue
            else:
                time.sleep(jittered(sleep))
                sleep = sleep * 2
                continue 

        reason = parse_status(response)

        if reason:
            return make_result(status=response.status_code,reason=reason)
        
        if response.status_code == 204:    # Success but no data (Delete)
            return make_result(True,204)   

      
        try:
            data = response.json()
        except ValueError:
            return make_result(status=response.status_code,reason='no json')

        
        return make_result(True,response.status_code,data,headers=dict(response.headers))

    return make_result(reason='max attempt reached')   # Optional just here so func dont't return None 
