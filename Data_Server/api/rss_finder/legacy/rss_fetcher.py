import json, urllib.request, sys, re
from urllib.parse import urlparse


###### TODO: buzzsprout, soundclound, iheartradio, listennotes, bbc sounds, spotify
###### Add proper search function

url=None
name=None
service=None

#isRunning will act as a flag to indicate whether the program has been run from the command line with arguments (in which case search functions should return only the most relevant result)
#or whether the user is interacting with the application (in which case multiple options should be presented)
isRunning = (len(sys.argv) == 1)

#Check if a podcast URL has been passed in

if len(sys.argv) == 2:
    url=sys.argv[1]
if len(sys.argv) == 3:
    name=sys.argv[1]
    service=sys.argv[2]
if len(sys.argv) > 3:
    print("Error: too many arguments")
    sys.exit()
    





###SERVICE SPECIFIC CLASSES###

class acast:
    service_name="acast"
    service_url="acast.com"
    
    def geturl(name):
        #Get URL from name
        return("https://play.acast.com/s/" + name)
    
    def getrss(url):
        #Get RSS feed from URL
        pieces=url.split("/")
        loc=len(pieces)-1
        return("https://rss.acast.com/" + pieces[loc])

class spreaker:
    service_name="spreaker"
    service_url="spreaker.com"
    
    def geturl(name):
        #Get URL from name
        return("https://www.spreaker.com/show/" + name)
    
    def getrss(url):
        try:
            #Get RSS feed from URL
            pieces=url.split("/")
            loc=len(pieces)-1
            podname=pieces[loc]
            
            api_url="https://api.spreaker.com/v2/shows/" + podname
            
            #Get JSON as bytes and convert to string
            response = urllib.request.urlopen(api_url)
            answer = response.read().decode()
            
            show = json.loads(answer)
            show_id = show["response"]["show"]["show_id"]
        
            return("https://www.spreaker.com/show/%d/episodes/feed" % show_id)
            
        except:
            print("Error: podcast not found.")
            exit()

class itunes:
    service_name="itunes"
    service_url="apple.com"
    
    def geturl(name):
        #With itunes, geturl() works slightly differently:
        #it uses the search function of the API and returns the first result
        
        #name = urllib.parse.quote(name)
        
        api_url="https://itunes.apple.com/search?term=" + name + "&entity=podcast"
        
        #Get JSON as bytes and convert to string
        response = urllib.request.urlopen(api_url)
        answer = response.read().decode()
        
        results = json.loads(answer)
        result = results["results"][0]
        collectionViewUrl = result["collectionViewUrl"].split("?")[0]
        
        return(collectionViewUrl)
    
    def getrss(url):
        try:
            #Get RSS feed from URL
            pieces=url.split("/")
            loc=len(pieces)-1
            podid=pieces[loc][2:]
            
            api_url="https://itunes.apple.com/lookup?id=" + podid
            
            #Get JSON as bytes and convert to string
            response = urllib.request.urlopen(api_url)
            answer = response.read().decode()
            
            results = json.loads(answer)
            feedUrl = results["results"][0]["feedUrl"]
            
        
            return(feedUrl)
            
        except:
            print("Error: podcast not found.")
            exit()
            
class podbean:
    service_name="podbean"
    service_url="podbean.com"
    
    def geturl(name):
        #Get URL from name
        return("https://" + name + ".podbean.com")
    
    def getrss(url):
        #Get RSS feed from URL
        feed = urllib.parse.urljoin(url, "feed")
        
        return(feed)

class listennotes:
    service_name="listennotes"
    service_url="listennotes.com"
    
    def geturl(name):
        #Get URL from name
        #This will work a little differently then the others - allowing a user to search for a podcast, and presenting options.
        pass
    
    def getrss(url):
        #Get RSS feed from URL
        pass

services = [acast, spreaker, itunes, podbean]


###GET RSS FEED###

def getrss(url):
    #Establish which service is being used
    p = urlparse(url)
    
    #Check if URL is in the right format
    if p.scheme == "":
        #URL not in correct format, add https:// to start of url
        url = "https://" + url
        p = urlparse(url)
    
    for s in services:
        if s.service_url in p.netloc:
            return s.getrss(url)
    
    print("Error: invalid hosting service.")
    exit()

def geturl(name,service):
    #Get URL for podcast
    for s in services:
        if s.service_name == service:
            return s.geturl(name)
            
    print("Error: invalid hosting service.")
    exit()

if url != None:
    print(getrss(url))
    exit()
else:
    if (name != None) and (service != None):
        #Get URL from name and service or ask for input
        url = geturl(name,service)
        print(getrss(url))
        exit()
    else:
        name = urllib.parse.quote(input("Please enter the name of the podcast: "))
        service = input("Please enter the name of the service which hosts the podcast: ")
        url = geturl(name,service)
        print(getrss(url))
        exit()


