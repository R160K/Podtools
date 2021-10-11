#engine
#NEW ENGINE
import asyncio
import aiohttp
from aiohttp import web
import api
import engine.async_if
import urllib.parse

async def respond(request):
    url = str(request.url)
    print("Path =", url)
    return await engine.async_if.respond(request, url)
    #return await api.respond(url)

async def home(request):
    with open("./engine/html/index.html", "r") as f:
        r = f.read()
    return web.Response(text=r, content_type="text/html")

def start_server():
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/{tail:.+}", respond)])

    web.run_app(app)
    
    try:
        engine.async_if.session.close()
        print("ClientSession closed.")
    except:
        pass
        
    print("Finished.")