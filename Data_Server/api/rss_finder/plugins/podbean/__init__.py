#api.rss_finder.plugins.podbean
import re, json
import urllib.parse
import general
import api.rss_finder as rss_finder
import engine.async_if as async_if
import api.rss_finder.plugins.common as common

def query_hook(queries):
    pattern = re.compile("(https?:\/\/)?.+\.podbean\.com\/?(feed)?$")
    
    if pattern.match(queries["url"]):
        print("Pattern matched (Podbean). Looking for RSS...")
        
        #Generate RSS URL
        url = queries["url"]
        if not url.startswith("http"):
            url = "https://" + url
        rss = urllib.parse.urljoin(url,"feed")
        print("RSS =",rss)
        
        #Extract showname from URL
        netloc = urllib.parse.urlparse(queries["url"]).netloc
        showname = netloc.split(".")[0]
        
        validate = True
        if "validate" in queries:
            if queries["validate"][0] == "False" or queries["validate"][0] == "false":
                validate = False
        
        data = {"rss": rss, "showname": showname, "redirect": queries["redirect"], "validate": validate}
        Obj = {"data": data, "func": return_feed}
        return Obj
    else:
        return None

# rss_finder.queryHooks += [query_hook]

async def return_feed(data):
    #Return show from url
    
    if data["redirect"]:
        #Redirect the user to the correct url
        Obj = general.resp_builder(Code=301, Headers={"Location": data["rss"]}, Body=None)
        return Obj
    else:
        if data["validate"]:
            print("Validating",data['rss'],"...")
            resp = await async_if.get_response(data["rss"], toRead=False)
            
            if resp.code == 200:
                if resp.headers["Content-Type"].startswith("text/xml"):
                    print("Validation successful.")
                    #Return the answer as JSON
                    Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(data))
                    return Obj
                else:
                    print("Validation failed: podcast not found.")
                    Obj = general.error_page(404, "The podcast could not be found on Podbean.")
                    return Obj
            else:
                print("Validation failed: an unexpected error occured.")
                Obj = general.error_page(resp.code, "An unexpected error occured. The Podbean feed %s could not be retrieved." % data["rss"])
                return Obj
        else:
            #Return the answer as JSON
            print("Validation disabled for:",data["rss"])
            Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(data))
            return Obj

common.set_up_query_hooks()