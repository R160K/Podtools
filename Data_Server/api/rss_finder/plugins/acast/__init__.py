#api.rss_finder.plugins.acast
import api.rss_finder as rss_finder
import general
import urllib.parse
import re
import json
import engine.async_if as async_if
import api.rss_finder.plugins.common as common

def query_hook(queries):
    pattern = re.compile("(https?:\/\/)?play.acast.com/s/.+")
    if pattern.match(queries["url"]):
        print("Pattern matched (acast). Looking for RSS...")
        
        validate = True
        if "validate" in queries:
            if queries["validate"][0] == "False" or queries["validate"][0] == "false":
                validate = False
        
        print("validate", validate)
        showname = queries["url"].split("play.acast.com/s/")[-1]
        
        #Generate rss feed from url
        rss = "https://rss.acast.com/" + showname
        
        data = {"rss": rss, "showname": showname, "redirect": queries["redirect"], "validate": validate}
        Obj = {"data": data, "func": return_feed}
        return Obj
    else:
        return None

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
                print("Validation successful.")
                #Return the answer as JSON
                Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(data))
                return Obj
            elif resp.code == 404:
                print("Validation failed: podcast not found.")
                Obj = general.error_page(404, "The podcast " + data["showname"]+ " could not be found on acast.")
                return Obj
            else:
                print("Validation failed: an unexpected error occured.")
                Obj = general.error_page(resp.code, "An unexpected error occured. The acast feed %s could not be retrieved." % data["rss"])
                return Obj
        else:
            #Return the answer as JSON
            print("Validation disabled for:",data["rss"])
            Obj = general.resp_builder(Code=200, Headers=general.JSON_HEADERS, Body=json.dumps(data))
            return Obj

common.set_up_query_hooks()