#api.spotify_tools.plugins.show_pseudo_rss.__init__
import general
import api
import api.spotify_tools as spotify_tools
import plugins
import urllib.parse
import api.spotify_tools.base as base
import api.spotify_tools.access as access
import engine.async_if as async_if
from api.spotify_tools.rss_builder import makeRSS, makeRSSShow, makeRSSEpisodes
import json

print("spotify_tools.show_pseudo_rss loading...")

def url_hook(path):
    print("api.spotify_tools.plugins.show_pseudo_rss.url_hook launched...")
    
    #Check if the /spotify/show endpoint has been requested and return the attached queries
    qtuple = general.isEndpoint(path, "/spotify/show", "QTuple")
    
    if qtuple and qtuple[0]:
        if "id" in qtuple[1].keys():
            #Check to see if either a market code or a refresh token has been supplied
            if "market" in qtuple[1].keys():                
                #Use client credentials authorisation flow
                data = {"ident": qtuple[1]["id"][0], "market": qtuple[1]["market"][0]}
                func = stream_show
                return {"data": data, "func": func, "streamed": True}
            elif "refresh_token" in qtuple[1].keys():
                #Use main authorisation flow with a refresh token
                data = {"ident": qtuple[1]["id"][0], "refresh_token": qtuple[1]["refresh_token"][0]}
                func = stream_show
                return {"data": data, "func": func, "streamed": True}
            else:
                msg = "Neither a market code nor a refresh token were provided."
                return {"data": general.error_page(400, msg, msg), "func": general.display_page}
        else:
            msg = "No show id provided."
            return {"data": general.error_page(400, msg, msg), "func": general.display_page}
    else:
        return None

spotify_tools.urlHooks += [url_hook]

async def stream_show(data):
    #1. Get access token
    if "market" in data.keys():
        market = data["market"]
        access_token = await access.get_token_cc()
        print("Got access token via client credentials flow.")
    elif "refresh_token" in data.keys():
        market = "from_token"
        access_token = await access.get_token_ac(data["refresh_token"])
        print("Got access token from refresh token.")
    else:
        raise Exception("Invalid request: neither market nor refresh_token included in query string. No access_token could be retrieved.")
    
    #2. Get show item (check if show exists)
    print("Getting show:",data["ident"],"in market",market)
    head = {"Authorization": "Bearer " + access_token}
    
    show_resp = await async_if.get_response("https://api.spotify.com/v1/shows/" + data["ident"] + "?market=" + market, headers=head)
    
    if not show_resp.code == 200:
        raise Exception("Error: show could not be found.")
    
    #TODO: PERHAPS FIND A WAY TO DO THIS ASYNC, WHILE WAITING FOR MORE DATA REQUESTS, OR IN A SEPARATE PROCESS
    
    
    offset = 0
    started = False
    finished = False
    

    while not finished:
        if not started:
            #Return headers, code, and first part of stream
            show = json.loads(show_resp.body)
            top = makeRSSShow(show)
            started = True
            yield {"Code": 200, "Headers": general.XML_HEADERS, "data": top}
        else:
            new_eps = await async_if.get_response("https://api.spotify.com/v1/shows/" + data["ident"] + "/episodes?limit=50&offset=" + str(offset) + "&market=" + market, headers=head)
            js = json.loads(new_eps.body)
            if len(js["items"]) == 50:
                #Go round again
                offset += 50
                rss = makeRSSEpisodes(js["items"])
                yield {"data": rss}
            else:
                finished = True
                rss = makeRSSEpisodes(js["items"], True)
                yield {"data": rss, "end": True}