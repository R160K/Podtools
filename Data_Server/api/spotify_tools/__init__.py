#api.spotify_tools.__init__
print("Spotify API initialising...")

import api, plugins
import general
import urllib.parse
import api.spotify_tools.access

#api.common must be imported as api.common because the package already contains a module called common
import api.common as common

#A local variable to hold "/spotify/" url hooks
urlHooks = []

#Define url parser and add it to the urlHooks list initialised by the api module
def url_hook(path):
    print("api.spotify_tools.url_hook launched...")
    
    if general.isAPI(path, "/spotify/"):
        print("Spotify URL hook triggered. Searching plugins...")
        for h in urlHooks:
            res = h(path)
            if res:
                return res
    else:
        return None

common.set_up_url_hooks()

print("...Spotify API loaded successfully!")