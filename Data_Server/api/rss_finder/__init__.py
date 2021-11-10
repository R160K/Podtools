#api.rss_finder.__init__.py

print("RSS Finder API initialising...")

import api, plugins
import urllib.parse
import general

import api.common as common

#A local variable to hold "/spotify/" url hooks
urlHooks = []
queryHooks = []

#Define url parser and add it to the urlHooks list initialised by the api module
def url_hook(path):
    print("api.rss_finder.url_hook launched...")
    
    query_tuple = general.isEndpoint(path, "/rss_finder/find", "QTuple")
    
    if query_tuple:
        queries = query_tuple[1]
        if "url" in queries:
            if "redirect" in queries:
                if queries["redirect"][0] == "False" or queries["redirect"][0] == "false":
                    redirect = False
                else:
                    redirect = True
            else:
                redirect = False
            
            queries["url"] = queries["url"][0]
            queries["redirect"] = redirect
            
            for q in queryHooks:
                res = q(queries)
                if res:
                    return res
    elif general.isAPI(path,"/rss_finder/"):
        #Pass it on to sub-packages
        print("RSS Finder URL hook triggered. Searching plugins...")
        for h in urlHooks:
            res = h(path)
            if res:
                return res
    else:
        return None


common.set_up_url_hooks()

print("...RSS Finder loaded successfully!")