#api.rss_finder.plugins.itunes
import re, json
import urllib.parse
import general
import api.rss_finder as rss_finder
import engine.async_if as async_if
import api.rss_finder.plugins.common as common

print("You're a fucking cunt!!!")

#TODO: Make sure no special characters can be included in itunes podcast url names
REGEX = "(https?:\/\/)?podcasts\.apple\.com\/\w+\/podcast\/[a-zA-Z\-]+\/id\d{10}$"
API_URL = "https://itunes.apple.com/lookup?id="
URL_PART = "rss_finder/find"

def query_hook(queries):
    pattern = re.compile(REGEX)
    
    if pattern.match(queries["url"]):
        print("Pattern matched (iTunes). Looking for RSS...")
        
        #Extract show id from URL
        showid = queries["url"][-10:]
        api = API_URL + showid
        
        #Extract show name from URL
        showname = queries["url"].split("/")[-2]
        
        validate = True
        if "validate" in queries:
            if queries["validate"][0] == "False" or queries["validate"][0] == "false":
                validate = False
        
        data = {"url": queries["url"], "api": api, "showid": showid, "showname": showname, "redirect": queries["redirect"], "validate": validate}
        Obj = {"data": data, "func": return_feed}
        return Obj
    else:
        return None

# rss_finder.queryHooks += [query_hook]

async def return_feed(data):
    showObj = await async_if.get_response(data["api"])
    
    if showObj.code == 200:
        js = json.loads(showObj.body)
        
        if js["resultCount"] >= 1:            
            rss = js["results"][0]["feedUrl"]
            
            if data["validate"]:
                cVU = js["results"][0]["collectionViewUrl"]
                bits = urllib.parse.urlparse(cVU)
                bits = bits._replace(query=None)
                cVU = urllib.parse.urlunparse(bits)
                
                if data["url"] != cVU:
                    print("It doesn't match!")
                    
                    q = urllib.parse.quote(cVU)
                    qurl = general.base_url.content + URL_PART + "?url=" + q
                    
                    Obj = general.resp_builder(Code=301, Headers={"Location": qurl}, Body=None)
                    return Obj
            
            if data["redirect"]:
                Obj = general.resp_builder(Code=301, Headers={"Location": rss}, Body=None)
                return Obj
            else:
                r = {"rss": rss, "showname": data["showname"], "redirect": data["redirect"], "validate": data["validate"]}
                Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(r))
                return Obj
        else:
            print("Podcast not found.")
            Obj = general.error_page(404, "The podcast %s with id %s could not be found on iTunes." % (data["showname"], data["showid"]))
            return Obj
    else:
        print("An unexpected error occurred.")
        Obj = general.error_page(show.code, "An unexpected error occurred. The iTunes feed %s could not be retrieved." % data["api"])
        return Obj

common.set_up_query_hooks()