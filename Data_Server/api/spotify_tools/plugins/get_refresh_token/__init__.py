#api.spotify_tools.plugins.get_refresh_token.__init__

#Get a refresh token for an individual user
#POTENTIALLY: save it as a cookie if a certain variable has been passed to the interpreter.

print("spotify_tools.get_refresh_token loading...")

scopes = "user-library-read%20user-read-private"
redirect_uri = "http://127.0.0.1:8080/spotify/get_token"


import general
import api.spotify_tools.base as base
import api.spotify_tools as spotify_tools
import urllib.parse
import api.spotify_tools.access as access
import general
import engine.async_if as async_if
import engine.signal as signal
import api.spotify_tools.plugins.common as common

HTML_HREF = "./api/spotify_tools/plugins/get_refresh_token/html/get_token.html"
html = signal.ValueLoader(HTML_HREF)

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

# spotify_tools.urlHooks += [url_hook]


async def spotify_login(data):
    url = base.authorise_url + "?response_type=code&show_dialog=true&scope=" + scopes + "&client_id=" + base.client_id.content + "&redirect_uri=" + redirect_uri
    
    Code = 303
    Headers = {"Location": url}
    Body = ""
    Obj = {"Code": Code, "Headers": Headers, "Body": Body}
    
    return Obj

async def get_token(data):
    try:
        refresh_token_js = await access.get_token_from_code(data["code"][0], redirect_uri, returnVar="JS")
    except access.TokenNotReturnedError as e:
        error_page = general.error_page(400, "BAD REQUEST: Spotify refused to give an access token for the given access code:<br /><div style='font-size:14pt'>%s</div>" % data["code"][0])
        resp = async_if.build_response(error_page)
        return resp
    
    refresh_token = refresh_token_js["refresh_token"]
    
    global html
    Body = html.content % refresh_token
    
    Code = 200
    Headers = general.HTML_HEADERS
    
    Obj = {"Code": Code, "Headers": Headers, "Body": Body}
    return Obj
    
    print("Refresh token:",refresh_token)


# def onload():
    # general.add_hook("api.spotify_tools", "urlHooks", url_hook)
    # print("api.spotify_tools.plugins.get_refresh_token loaded successfully.")

# def cleanup():
    # print("Cleaning up api.spotify_tools.plugins.get_refresh_token...")
    # spotify_tools.urlHooks.remove(url_hook)

common.set_up_url_hooks()