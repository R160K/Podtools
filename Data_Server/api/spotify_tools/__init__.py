#api.spotify_tools.__init__
print("Spotify API initialising...")

import api, plugins
import general
import urllib.parse
import api.spotify_tools.access

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


api.urlHooks += [url_hook]

#Load plugins for this package
packages = plugins.get_plugins("api\\spotify_tools\\plugins")
plugins.load_plugins(packages)

print("urlHooks:",urlHooks)

print("...Spotify API loaded successfully!")