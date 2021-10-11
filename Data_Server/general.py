#Functions and classes for general use.
import urllib.parse


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

#A few boilerplate parts of responses
XML_HEADERS = (("Content-type","text/xml"),("charset","utf-8"))
HTML_HEADERS = (("Content-type","text/html"),("charset","utf-8"))
JSON_HEADERS = (("Content-type","application/json"),("charset","utf-8"))

def error_page(code, title, message):
    with open("./engine/html/error.html", "r") as f:
        Body = f.read() % (title, message)
    
    Headers = HTML_HEADERS
    Code = code
    return resp_builder(Code, Headers, Body)
    
def resp_builder(Code, Headers, Body):
    return {"Code": Code, "Headers": Headers, "Body": Body}

async def display_page(data):
    return data