#engine.signal

import engine.async_if as async_if
import general
import urllib.parse
import aiofiles
import plugins
import traceback, sys
import importlib
import os
from configparser import ConfigParser

#List of async reload functions for html/rss templates and secrets etc.
reload_hooks = []
valueLoaders = []

testy = "hidden"

class ValueLoader():
    def __init__(self, href, add_to_list=True):
        #HACK: change href depending on system
        if href.startswith("../secrets/") and not os.path.isdir("../secrets"):
            href = "/home/secrets/" + href.split("../secrets/")[1]
        elif href.startswith("../public/") and not os.path.isdir("../public"):
            href = "/home/public/" + href.split("../public/")[1]
            
        self.href = href
        
        with open(href, "r") as f:
            self.content = f.read()
        
        if add_to_list:
            global reload_hooks
            reload_hooks += [self.reload]
            
            global valueLoaders
            valueLoaders += [self]
    
    async def reload(self):
        async with aiofiles.open(self.href, "r") as f:
            self.content = await f.read()

THUMB_UP_HREF = "./engine/html/thumb_up.html"
thumb_up = ValueLoader(THUMB_UP_HREF)

SIGNAL_SECRET_HREF = "../secrets/signal_secret.txt"
signal_secret = ValueLoader(SIGNAL_SECRET_HREF)

async def process_signal(data):
    #BLANK - this is not a DOCSTRING.
    
    '''
        SIGNALS:
            -Refresh_Assets [ValueLoader1] [ValueLoader2] [ValueLoader3]...
                Refresh engine.signal.ValueLoaders - HTML/RSS templates as well as "public" and "secrets".
                If no args are supplied or only "ALL" is supplied, refreshes all assets in valueLoaders. Else refreshes only named valueLoaders (so long as they are in valueLoaders).
            -Remove_Hook hook array
                Remove hook "hook" from list "array".
            -Unload_Module module
                Unload module "module".
    '''
    
    print("Signal called.")
    
    qs = data.decode("utf-8")
    queries = urllib.parse.parse_qs(qs)
    
    print(queries)
    
    try:
        assert queries["signal_secret"][0] == signal_secret.content
        print("Valid signal received.")
        
        sig_parts = queries["signal"][0].split(" ")
        sig = sig_parts[0]
        args = sig_parts[1:]
        
        #SETTERS
        if sig == "-Refresh_Assets":
            # -Refresh_Asset ValueLoader1 [ValueLoader2] [ValueLoader3]...
            #Refreshes specified asset(s). If no asset is specified, refreshes all assets.
            await refresh_assets(args)
        elif sig == "-Load_Modules":
            await load_modules(args)
        elif sig == "-Unload_Modules":
            await unload_modules(args)
        elif sig == "-Load_Plugins":
            await load_plugins(args)
        elif sig == "-Load_All_Plugins":
            await load_all_plugins()
        elif sig == "-Unload_Plugins":
            await unload_plugins(args)
        elif sig == "-Remove_Hooks":
            print("-Remove_Hooks called.")
            await remove_hooks(args)
        elif sig == "-SetAttr":
            # setattr(args[0], args[1], args[2])
            # print(testy)
            pass
            
        #GETTERS
        elif sig == "-GetAttr":
            pass
        else:
            raise Exception("BAD REQUEST")
        
        global thumb_up
        resp = general.resp_builder(200, general.HTML_HEADERS, thumb_up.content)
        response = async_if.build_response(resp)
        return response
    except Exception as e:
        print(traceback.format_exc())
        error_page = general.error_page(400, "BAD REQUEST: Invalid signal request made.")
        response = async_if.build_response(error_page)
        return response
    
async def refresh_assets(args):
    if len(args) == 0 or "ALL" in args:
        assets = valueLoaders
    else:
        assets = [x for x in valueLoaders if x.href in args]
    
    for a in assets:
        await a.reload()

async def load_modules(args):
    reloads = [sys.modules[x] for x in args if x in sys.modules]
    loads = [x for x in args if not x in sys.modules]
    
    for m in reloads:
        importlib.reload(m)
    
    for m in loads:
        importlib.load_module(m)

async def unload_modules(args):
    unloads = [x for x in args if x in sys.modules]
    
    for m in unloads:
        del sys.modules[m]

async def load_plugins(args):
    #TODO: currently only works with dirs, make work with names as well
    _plugins = []
    
    for a in args:
        print("Trying", a)
        try:
            pf = os.path.join(a, "file.plugin")
            async with aiofiles.open(pf, "r") as f:
                raw_config = await f.read()
            parser = ConfigParser()
            parser.read_string(raw_config)
            _plugins += [(a, parser)]
        except Exception as e:
            try:
                pb = plugins.__PLUGINS[a].location
                pf = os.path.join(pb, "file.plugin")
                async with aiofiles.open(pf, "r") as f:
                    raw_config = await f.read()
                parser = ConfigParser()
                parser.read_string(raw_config)
                _plugins += [(a, parser)]
            except:
                print("Error importing plugin:", a, "\n", e.__class__.__name__)
    
    loads = []
    reloads = []
    
    for p in _plugins:
        name = p[1]["PLUGIN"]["name"]
        if name in plugins.__PLUGINS:
            reloads += [plugins.__PLUGINS[name]]
        else:
            loads += [p[0]]
    
    if reloads:
        plugins.reload_plugins(*reloads)
    
    if loads:
        plugins.load_plugins(loads)

async def unload_plugins(args):
    _plugins = []
    
    for a in args:
        print("Trying", a)
        try:
            pf = os.path.join(a, "file.plugin")
            async with aiofiles.open(pf, "r") as f:
                raw_config = await f.read()
            parser = ConfigParser()
            parser.read_string(raw_config)
            _plugins += [(a, parser)]
        except Exception as e:
            try:
                pb = plugins.__PLUGINS[a].location
                pf = os.path.join(pb, "file.plugin")
                async with aiofiles.open(pf, "r") as f:
                    raw_config = await f.read()
                parser = ConfigParser()
                parser.read_string(raw_config)
                _plugins += [(a, parser)]
            except:
                print("Error reading plugin:", a, "\n", e.__class__.__name__)
    
    unloads = []
    
    for p in _plugins:
        name = p[1]["PLUGIN"]["name"]
        if name in plugins.__PLUGINS:
            unloads += [plugins.__PLUGINS[name]]
    
    plugins.unload_plugins(*unloads)
    
async def load_all_plugins():
    #WARNING: THIS IS A BLOCKING FUNCTION
    packages = plugins.get_plugins("api")
    _plugins = plugins.load_plugins(packages,returnVar=1)

async def remove_hooks(args):
    hooks = args[::2]
    arrays = args[1::2]
    
    for i in range(0, len(hooks)):
        h = hooks[i]
        a = arrays[i]
        
        try:
            h_name = h.split(".")[-1]
            h_mod = h[:-(len(h_name)+1)]
            
            hook = getattr(sys.modules[h_mod], h_name)
            
            a_name = a.split(".")[-1]
            a_mod = a[:-(len(a_name)+1)]
            
            array = getattr(sys.modules[a_mod], a_name)
            
            
            array.remove(hook)
            print("Successfully removed %s from %s." % (h, a))
        except:
            print("Error removing %s from %s." % (h, a))

print("engine.signal imported successfully.")