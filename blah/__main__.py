from aiohttp import web

async def index(request):
    return web.Response(text="blah blah blah blah blah", content_type="text/html")

app = web.Application()
app.add_routes([web.get("/", index)])