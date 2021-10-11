#api.spotify_tools.plugins.get_refresh_token.__init__

#Get a refresh token for an individual user
#POTENTIALLY: save it as a cookie if a certain variable has been passed to the interpreter.

print("spotify_tools.get_refresh_token loading...")

scopes = "user-library-read"
redirect_uri = "http://127.0.0.1:8080/spotify/get_token"
#redirect_uri = "http://127.0.0.1:8080/spotify/get_token"

html = "./api/spotify_tools/plugins/get_refresh_token/html/get_token.html"

import general
import api.spotify_tools.base as base
import api.spotify_tools as spotify_tools
import urllib.parse
import api.spotify_tools.access as access

def url_hook(path):
    print("api.spotify_tools.plugins.get_refresh_token.url_hook launched...")
    queries = general.isEndpoint(path, "/spotify/get_token", returnVar="Queries")
    truth = general.isEndpoint(path, "/spotify/get_token", returnVar="True")
    
    if truth:
        if "code" in queries:
            Obj = {"data": queries, "func": get_token}
            return Obj
        else:
            #No access code in url query string. Redirect to Spotify to get one.
            Obj = {"data": None, "func": spotify_login}
            return Obj
    else:
        return None

spotify_tools.urlHooks += [url_hook]


async def spotify_login(data):
    url = base.authorise_url + "?response_type=code&show_dialog=true&scope=" + scopes + "&client_id=" + base.client_id + "&redirect_uri=" + redirect_uri
    
    Code = 301
    Headers = {"Location": url}
    Body = ""
    Obj = {"Code": Code, "Headers": Headers, "Body": Body}
    
    return Obj

async def get_token(data):
    refresh_token_js = await access.get_token_from_code(data["code"][0], redirect_uri, returnVar="JS")
    
    refresh_token = refresh_token_js["refresh_token"]
    
    with open(html, "r") as f:
        Body = f.read() % refresh_token
    
    Code = 200
    Headers = general.HTML_HEADERS
    
    Obj = {"Code": Code, "Headers": Headers, "Body": Body}
    return Obj
    
    print("Refresh token:",refresh_token)

print("spotify_tools.get_refresh_token loaded.")