#plugin loader

from dataclasses import dataclass
import os, importlib, re
from configparser import ConfigParser
import traceback
import sys

def dummy():
    pass

@dataclass
class plugin:
    name : str
    purpose : str
    priority : int
    
    location : str
    
    path : str
    __module__ : object = None

#A function to add special properties to plugin class that hold either functions or names of functions and default to dummy.
def add_prop(prop_name, default_value=dummy):
    var_name = "__" + prop_name
    setattr(plugin, var_name, default_value)
    
    @property
    def prop(self):
        var = getattr(self, var_name)
        func_type = type(dummy)
        
        if isinstance(var, str):
            if var == "None":
                return dummy
            
            try:
                cleanup_func = getattr(self.__module__, var)
                assert isinstance(cleanup_func, func_type)
                
                return cleanup_func
            except:
                return dummy
        elif isinstance(var, func_type):
            return var
        else:
            return dummy
        
        return getattr(self, var_sname)
    
    @prop.setter
    def prop(self, s):
        setattr(self, var_name, s)
    
    @prop.deleter
    def prop(self):
        setattr(self, var_name, default_value)
    
    setattr(plugin, prop_name, prop)

#Add some properties to plugins
add_prop("onload") #Triggered once the package has been loaded.
add_prop("cleanup") #There to do some tidying up when a plugin is plugged out.

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
            
            #Check the dependencies required by the plugin are already loaded
            #NOTE: Currently only works for dependencies imported in the same directory.
            #TODO: split load plugins into a separate function so that all plugins are primed first and then all loaded according to priority.
            #May require plugin directory to be added to file.plugin so that sub-plugins are primed automatically and then attached to their parents during loading
            #Depedency checking must happen after plugins have been sorted.
            # if "dependencies" in parser['PLUGIN']:
                # deps = parser['PLUGIN']['dependencies']
                # for dep in deps:
                    # if not (dep in __plugins or dep in __PLUGINS):
                        # raise Exception("The dependencies for this plugin were not met.")
            
            #Check if the path variable is set in file.plugin. If not, create a default one
            path = ""
            if "path" in parser['PLUGIN']:
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
            
            p = plugin(name=name, purpose=purpose, priority=priority, path=path, location=d)
            
            if "cleanup" in parser['PLUGIN']:
                p.cleanup = parser['PLUGIN']['cleanup']
            
            if "onload" in parser['PLUGIN']:
                p.onload = parser['PLUGIN']['onload']
            
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
                
                #Trigger onload function of plugin
                p[1].onload()
        except Exception as e:
            raise e
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

def unload_plugins(*p):
    names = [x.name for x in p]
    print("Unloading plugins:", names)
    r = [x for x in __PLUGINS]
    print("Before:", r)
    for x in p:
        n = x.name
        x.cleanup()
        del sys.modules[n]
        if n in __PLUGINS:
            del __PLUGINS[n]
        print(n, "has been unloaded.")
    
    print("Unloading complete!")
    r = [x for x in __PLUGINS]
    print("After:", r)

def reload_plugins(*p):
    names = [x.name for x in p]
    print("Reloading plugins:", names)
    dirs = []
    
    for x in p:
        dirs += [x.location]
        unload_plugins(x)
    
    print("Plugins unloaded. Loading now...")
    load_plugins(dirs)

print("Plugins module imported successfully.")