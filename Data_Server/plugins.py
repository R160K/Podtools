#plugin loader

from dataclasses import dataclass
import os, importlib, re
from configparser import ConfigParser
import traceback

@dataclass
class plugin:
    name : str
    purpose : str
    priority : int
    
    path : str
    __module__ : object = None

#A list of all currently loaded plugins
__PLUGINS = {}

def get_plugins(path):
    #Get a list of files and directories in the given path
    files = os.listdir(path)
    
    #Cycle through to get a list of directories with a file.plugin file
    dirs = []
    for f in files:
        g = os.path.join(path,f)
        if os.path.isdir(g):
            h = os.path.join(g,"file.plugin")
            if os.path.isfile(h):
            #f is a directory with a file.plugin file
                dirs += [g]
    
    print("Plugins found:",dirs)
    return dirs
    
def load_plugins(dirs, updatePLUGINS=True, returnVar=0, verbose=True):
    """
    Load a given list of packages.
    
    Parameters
    ----------
    dirs : list
        Required: A list of urls for package directories.
    updatePLUGINS : bool = True
        Optional: If True plugins will be added to the global __PLUGINS variable. If False they will not.
    returnVar : int = 0
        Optional: Dictates which variable to return. If set to 0 (default) will return locally created __plugins variable. Else will return global __PLUGINS variable.
    verbose : bool = True
        Optional: Dictates whether to print progress being made in processing plugins.
    
    Returns
    -------
    dict
        A dictionary containing either just the plugins loaded by the current invocation of the load_plugins method (__plugins) or the global plugin list (__PLUGINS) depending on the value of returnVar.
    """
    #Read file.plugin files and import plugins
    global __PLUGINS
    __plugins = {}
    
    for d in dirs:
        try:
            parser = ConfigParser()
            config_file = os.path.join(d,"file.plugin")
            parser.read(config_file)
            
            #Check if the path variable is set in file.plugin. If not, create a default one
            path = ""
            if "path" in parser['PLUGIN'].keys():
                path = parser['PLUGIN']['path']
            else:
                #Split d into directory names and join with "." to get python loadable address
                #Split by both "/" and "\\" using a regular expression
                myREGEX = "/|\\\\"
                path_pieces = re.split(myREGEX, d)
                path = ".".join(path_pieces)
            
            name=parser['PLUGIN']['name']
            purpose=parser['PLUGIN']['purpose']
            priority=int(parser['PLUGIN']['priority'])
            
            p = plugin(name=name, purpose=purpose, priority=priority, path=path)
            __plugins.update({parser['PLUGIN']['name']: p})
            if verbose:
                print(config_file, "primed for loading.")
        except Exception as e:
            if verbose:
                print("Error: %s could not be primed." % d)
                print(e.__class__.__name__)
    
    #Sort plugins by priority and load them in order
    priority_list = sorted(__plugins.items(), key=lambda k:k[1].priority)
    for p in priority_list:
        try:
            p[1].__module__ = importlib.import_module(p[1].path)
            if verbose:
                print(p[0], "loaded successfully.")
        except Exception as e:
            if verbose:
                print(p[0], "could not be loaded.")
                print(p[1].path)
                print(e.__class__.__name__)
                traceback.print_tb(e.__traceback__)
    
    if updatePLUGINS:
        __PLUGINS.update(__plugins)
    
    if returnVar:
        return __PLUGINS
    else:
        return __plugins
    
print("Plugins module imported successfully.")