#api.rss_finder.__init__.py

#TODO: set up plugin architecture for this API.
print("RSS Finder API initialising...")

import api, plugins
import urllib.parse
import general

#Define url parser and add it to the urlHooks list initialised by the api module
def url_hook(path):
    print("api.rss_finder.url_hook launched...")
    
    if general.isAPI(path,"/rss_finder/"):
        return "RSS Finder mothafucka!!!"
    else:
        return None

api.urlHooks += [url_hook]

print("...RSS Finder loaded successfully!")