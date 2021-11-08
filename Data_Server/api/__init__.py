#api.__init__.py
print("Initiating APIs...")
urlHooks = []

#Load each package in the api directory using plugins module.
import plugins
_plugins = plugins.do_it_all("api")

import engine.async_if as async_if
import urllib.parse

def check_path(path):
    print("api.__init__.check_path","called.")
    print("Check path launched:",path)
    
    my_res = None
    for h in urlHooks:
        res = h(path)
        if res:
            my_res = res
            break
    
    return my_res

async def respond(path):
    '''
    A function to check the path given against all loaded urlHooks. This function is called from the engine module.
    
    Parameters
    ----------
    path : str
        Required: The path asked for in the request.
    give_response : function
        Required: The function to trigger in order to write the response to the request.
    passthrough : object
        Optional: An object to be passed to the give_response function.
    '''
    my_res = check_path(path)
    
    if my_res:
        #Check to see if the result should be streamed
        if "streamed" in my_res and my_res["streamed"] == True:
            print(my_res)
            print("Streaming now...")
            
            # async for p in my_res["func"](my_res["data"]):
                # with open("./logloglog.rss", "ab") as f:
                    # f.write(p["data"])
            
            srp = async_if.stream_response_prep(my_res["data"], my_res["func"])
            return srp
        else:
            x = await my_res["func"](my_res["data"])
            return x
    else:
        p = urllib.parse.urlparse(path).path
        r = async_if.build_404(p)
    
    return r

print("APIs ready!")