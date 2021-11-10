#api.rss_finder.plugins.spreaker
import re, json
import urllib.parse
import general
import api.rss_finder as rss_finder
import engine.async_if as async_if
import api.rss_finder.plugins.common as common

API_URL="https://api.spreaker.com/v2/shows/"

def query_hook(queries):
    pattern = re.compile("(https?:\/\/)?(www\.)?spreaker\.com\/show\/.+")
    
    if pattern.match(queries["url"]):
        print("Pattern matched (Spreaker). Looking for RSS...")
        
        showname = queries["url"].split("spreaker.com/show/")[1]
        
        data = {"api": API_URL + showname, "showname": showname, "redirect": queries["redirect"]}
        Obj = {"data": data, "func": return_feed}
        return Obj
    else:
        return None

# rss_finder.queryHooks += [query_hook]

async def return_feed(data):
    #Request show data from the Spreaker API
    show = await async_if.get_response(data["api"])
    
    if show.code == 200:
        js = json.loads(show.body)
        show_id = js["response"]["show"]["show_id"]
        rss = "https://www.spreaker.com/show/%d/episodes/feed" % show_id
        
        if data["redirect"]:
            Obj = general.resp_builder(Code=301, Headers={"Location": rss}, Body=None)
            return Obj
        else:
            r = {"rss": rss, "showname": data["showname"], "redirect": data["redirect"], "validate": True}
            Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(r))
            return Obj
    elif show.code == 404:
        print("Podcast not found.")
        Obj = general.error_page(404, "The podcast %s could not be found on Spreaker." % data["showname"])
        return Obj
    else:
        print("An unexpected error occurred.")
        Obj = general.error_page(show.code, "An unexpected error occurred. The Spreaker feed %s could not be retrieved." % data["api"])
        return Obj

common.set_up_query_hooks()