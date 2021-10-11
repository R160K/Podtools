import argparse, importlib

engine = None
async_if = None

def load_engine(args=None):
    import argparse
    global engine, async_if
    #Create an argument parser and set the options and arguments to accept
    parser = argparse.ArgumentParser(description="Start the Podcast Tools API server.", )
    parser.add_argument("-e","--engine", default="engine") #Accept arguments -e and --engine, which tell the program which engine module to use (default is "engine").
    parser.add_argument("-a","--async_if", default="engine.async_if") #Set non-defaul async_if.py file
    
    #If args have been passed to this function, parse those args. Else, parse command line args.
    my_args = None
    
    if args:
        my_args = parser.parse_args(args)
    else:
        my_args = parser.parse_args()
    
    #Set my_engine to the value of the engine argument (default is "engine").
    my_engine = my_args.engine
    my_async = my_args.async_if
    
    #Try to load the engine, check it has the "start_server" attribute, and import the api module
    try:
        the_engine = importlib.import_module(my_engine)
        if not (hasattr(engine,"start_server")):
            raise AttributeError("The engine provided has no 'start_server' attribute.")
    except ModuleNotFoundError as e:
        print("Invalid engine:",my_engine)
        print(e.__class__.__name__,":",e.args[0])
        exit()
    except AttributeError as e:
        print("Invalid engine:",my_engine)
        print(e.__class__.__name__,":",e.args[0])
        exit()
    
    try:
        the_async = importlib.import_module(my_async)
    except ModuleNotFoundError as e:
        print("Invalid async_if:",my_async)
        print(e.__class__.__name__,":",e.args[0])
        exit()
        
    
    engine = the_engine
    async_if = the_async
    
    return engine, async_if