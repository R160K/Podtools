#engine.async_if
#NEW ENGINE
import asyncio
import aiohttp
from aiohttp import web
import api

#Create variable for the web request client (can only be  
session = None

async def get_session():
    #If a web request client has not yet be created, create one
    global session
    if not session:
        session = aiohttp.ClientSession()
    
    return session

async def get_response(url,headers=None):
    session = await get_session()
    
    resp = await session.get(url, headers=headers)
    body = await resp.text()
    
    r = web_response(resp, body)
    return r

async def post_response(url,headers=None,data=None):
    session = await get_session()
    
    resp = await session.post(url,headers=headers,data=data)
    body = await resp.text()
    
    r = web_response(resp, body)
    return r


def build_response(data):
    return web.Response(body=data["Body"], headers=data["Headers"], status=data["Code"])

def build_404(endpoint):
    with open("./engine/html/404.html", "r") as f:
        text = f.read() % endpoint
    return web.Response(text=text, content_type="text/html", status=404)


async def stream_response(srp, request):
    response = None
    
    async for g in srp.gen(srp.data):
        # with open("./logloglog.rss", "ab") as f:
            # f.write(g["data"])
        
        if "Code" in g:
            response = web.StreamResponse(status=g["Code"], headers=g["Headers"])
            await response.prepare(request)
        
        await response.write(g["data"])
            
        
    return response

async def respond(request, url):
    #A function to check what sort of response is being returned:
    #If a web.Response object, pass it back no problem.
    a = await api.respond(url)
    
    if a.__class__.__name__ == "Response":
        return a
    elif a.__class__.__name__ == "dict":
        response = build_response(a)
        return response
    elif a.__class__.__name__ == "stream_response_prep":
        response = await stream_response(a, request)
        return response
    else:
        raise Exception("Dodgy response from api.respond.")


#Class for passing responses back to other modules
class web_response:
    def __init__(self, resp, body):
        self.code = resp.status
        self.body = body
        
        self.headers = {}
        for h in resp.raw_headers:
            self.headers.update({h[0].decode("utf-8"): h[1].decode("utf-8")})
        
        self.response = resp
    
    def __set_vals__(self, code, headers, body):
        self.code = code
        self.headers = headers
        self.body = body

class stream_response_prep:
    def __init__(self, data, func):
        self.data = data
        self.gen = func
