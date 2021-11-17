#Functions and classes for general use.
import urllib.parse
import engine.signal as signal
import sys, inspect

ERR_PAGE_HREF = "./engine/html/error.html"
err_page = signal.ValueLoader(ERR_PAGE_HREF)

BASE_URL_HREF = "../public/base_url.txt"
base_url = signal.ValueLoader(BASE_URL_HREF)

ALLOW_ORIGIN_HREF = "../public/allow_origin.txt"
allow_origin = signal.ValueLoader(ALLOW_ORIGIN_HREF)

###URL CHECKERS###

#Function to check if a given "path" begins with a given "sought".
#NOTE: If "sought" does not end with a "/", returns False.
def isAPI(path,sought):
    #Check if "sought" ends with a "/".
    if sought[-1] != "/":
        return False
    else:
        url_pieces = urllib.parse.urlparse(path)
        my_path = url_pieces.path
        
        #Check if "path" begins with "sought".
        if my_path[:len(sought)] == sought:
            return True
        else:
            return False

#Function to check if a given "path" equals a given "sought".
def isEndpoint(path,sought,returnVar="True"):
    """
    Check if the path of a url is the same as the value of "sought", (i.e. check if "path" and "sort" have the same API endpoint), and return either a value of False, or an affirmative value of the requested type.
    
    Parameters
    ----------
    path : str
        Required: the url to be evaluated.
    sought : str
        Required: the endpoint path for the url to be checked against.
    returnVar : str = "True"
        Optional: the sort of value to return. Options are:
            "True": returns True.
            "Pieces": returns the pieces of the parsed url.
            "Queries": returns the parsed queries from the url query string.
            "Path": returns the path that was evaluated.
            "QTuple": returns a tuple of (True, parsed queries)
        Returns True if any other value is given.
    """
    url_pieces = urllib.parse.urlparse(path)
    my_path = url_pieces.path
    
    if my_path == sought:
        if returnVar == "True":
            return True
        elif returnVar == "Pieces":
            return url_pieces
        elif returnVar == "Queries":
            queries = urllib.parse.parse_qs(url_pieces.query)
            return queries
        elif returnVar == "Path":
            return path
        elif returnVar == "QTuple":
            queries = urllib.parse.parse_qs(url_pieces.query)
            return(True,queries)
        else:
            return True
    else:
        return False



###PAGE BUILDERS###

#A few boilerplate parts of responses
XML_HEADERS = (("Content-type","text/xml"),("charset","utf-8"),("Access-Control-Allow-Origin", allow_origin.content),("blah", "blah"))
HTML_HEADERS = (("Content-type","text/html"),("charset","utf-8"),("Access-Control-Allow-Origin", allow_origin.content))
JSON_HEADERS = (("Content-type","application/json"),("charset","utf-8"),("Access-Control-Allow-Origin", allow_origin.content))

    
def resp_builder(Code, Headers, Body):
    return {"Code": Code, "Headers": Headers, "Body": Body}

async def display_page(data):
    return data

def fill_template(temp, d):
    pre = temp
    for k in d:
        pre = pre.replace("{"+k+"}", d[k])
    
    return pre

def error_page(code, message, title="Oooops..."):
    d = {"err_num": str(code), "title": title, "message": message}
    
    global err_page
    o = fill_template(err_page.content, d)
    
    Headers = HTML_HEADERS
    
    return resp_builder(code, Headers, o)



###HOOK SYSTEM###

def add_hook(modname, listname, hook):
    l = getattr(sys.modules[modname], listname)
    l += [hook]

def hooker(modname, listname, hookname):
    def wrapper(func):
        def new_func():
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            hook = getattr(mod, hookname)
            
            print("Called by: %s." % mod.__name__)
            
            def onload():
                add_hook(modname, listname, hook)
                print("%s loaded successfully." % mod.__name__)
            
            def cleanup():
                print("Cleaning up %s..." % mod.__name__)
                l = getattr(sys.modules[modname], listname)
                l.remove(hook)
            
            func()
            
            setattr(mod, "onload", onload)
            setattr(mod, "cleanup", cleanup)
        return new_func
    return wrapper