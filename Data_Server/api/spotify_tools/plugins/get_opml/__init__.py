#api.spotify_tools.plugins.get_opml
import general
import api.spotify_tools.plugins.common as common
import api.spotify_tools.access as access
import engine.async_if as async_if
import json
import tools.opml as opml

print("spotify_tools.get_opml loading...")

URL_PART = "spotify/show"

def url_hook(path):
    print("api.spotify_tools.plugins.get_opml.url_hook launched...")
    
    #Check if the /spotify/get_opml has been requested and return the attached queries
    qtuple = general.isEndpoint(path, "/spotify/opml", "QTuple")
    
    if qtuple and qtuple[0]:
        if "refresh_token" in qtuple[1].keys():
            data = {"refresh_token": qtuple[1]["refresh_token"][0]}
            func = get_opml
            
            return {"data": data, "func": func}
        else:
            msg = "BAD REQUEST: No refresh token provided."
            return {"data": general.error_page(400, msg), "func": general.display_page}
    else:
        return None

async def get_opml(data):
    print("Starting it...")
    #1. Get access token
    # market = "from_token"
    
    try:
        access_token = await access.get_token_ac(data["refresh_token"])
    except access.TokenNotReturnedError as e:
        print("TokenNotReturnedError")
        msg = "BAD REQUEST: Spotify refused an access token with the given refresh token:<br />%s" % data["refresh_token"]
        return  general.error_page(400, msg)
    except access.TokenResponseError as e:
        print("TokenResponseError")
        msg = "ERROR: Spotify did not respond to the request."
        return general.error_page(500, msg)
    
    print("Got access token from refresh token.")
    
    
    #2. Get the correct market for the user
    head = {"Authorization": "Bearer " + access_token}
    
    user_info = await async_if.get_response("https://api.spotify.com/v1/me", headers=head)
    
    try:
        ui = json.loads(user_info.body)
    except:
        msg = "ERROR: Spotify did not provide a valid response to the request."
    
    if not user_info.code == 200:
        err = ui["error"]
        msg = "SPOTIFY ERROR: " + err["message"]
        return general.error_page(err["status"], msg)
        
    market = ui["country"]
    print("COUNTRY:", market)
    
    
    #3. Get list of podcasts the user has subscribed to
    show_dicts = []
    
    offset = 0
    finished = False
    
    while not finished:
        shows = await async_if.get_response("https://api.spotify.com/v1/me/shows?offset=" + str(offset) + "&limit=5", headers=head)
        js = json.loads(shows.body)
        
        base_url = general.base_url.content
        spotify_base_url = "https://play.spotify.com/show/"
        
        for s in js["items"]:
            show_id = s["show"]["id"]
            show_name = s["show"]["name"]
            
            xmlurl = base_url + URL_PART + "?id=" + show_id + "&market=" + market
            
            htmlurl = spotify_base_url + show_id
            
            text = show_name
            title = show_name
            
            d = {"text": show_name, "title": show_name, "xmlurl": xmlurl, "htmlurl": htmlurl}
            
            show_dicts += [d]
        
        if len(js["items"]) == 5:
            #Go round again
            offset += 5
        else:
            finished = True
    
    outlines = []
    
    for i in show_dicts:
        outlines += [i]
    
    my_opml = opml.make_opml("My Spotify subs.", outlines)
    
    with open("logloglog", "wb") as f:
        f.write(my_opml)
    
    Obj = general.resp_builder(Code = 200, Headers = general.XML_HEADERS, Body = my_opml)
    return Obj

common.set_up_url_hooks()