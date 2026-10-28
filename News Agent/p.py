import httpx


r = httpx.get('https://r.jina.ai/https://en.wikipedia.org/wiki/Hello')
print(r)