#engine

import asyncio
import aiohttp, aiofiles
from aiohttp import web
import api
import engine.async_if
import urllib.parse
import engine.signal as signal

async def respond(request):
    url = str(request.url)
    print("Path =", url)
    return await engine.async_if.respond(request, url)


HOME_INDEX_HREF = "./engine/html/index.html"
home_index = signal.ValueLoader(HOME_INDEX_HREF)

async def home(request):
    global home_index
    return web.Response(text=home_index.content, content_type="text/html")

async def signal_r(request):
    data = await request.read()
    
    response = await signal.process_signal(data)
    return response

def start_server():
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/{tail:.+}", respond)])
    app.add_routes([web.post("/{tail:.*}", signal_r)])
    
    web.run_app(app)
    
    try:
        engine.async_if.session.close()
        print("ClientSession closed.")
    except:
        pass
        
    print("Finished.")

def get_server():
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/{tail:.+}", respond)])
    app.add_routes([web.post("/{tail:.*}", signal_r)])
    
    return app

async def start_server2():
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/{tail:.+}", respond)])
    
    loop = asyncio.get_event_loop()
    runner = aiohttp.web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    

async def main():
    app = web.Application()
    app.add_routes([web.get("/", home)])
    app.add_routes([web.get("/{tail:.+}", respond)])
    
    await asyncio.gather(web._run_app(app))
    
    await close_client()

        
    print("Finished.")

def start_server3():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        l = asyncio.new_event_loop()
        l.run_until_complete(close_client())
    
    print("Finished.")

async def close_client():
    try:
        await engine.async_if.session.close()
        print("ClientSession closed.")
    except:
        pass