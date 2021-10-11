#api.spotify_tools.rss_builder
#Build an RSS feed from a Spotify show object and a list of Spotify episode objects
f = open("./api/spotify_tools/rss_templates/head.rss")
head = f.read()
f.close()

f = open("./api/spotify_tools/rss_templates/foot.rss")
foot = f.read()
f.close()

f = open("./api/spotify_tools/rss_templates/episode.rss")
ep_template = f.read()
f.close()

stock_mp3 = "https://download1645.mediafire.com/njvgj0wvfybg/v8cw2s4et4ivvxs/spotify_stock.mp3"

def makeRSS(show,episodes):
    #Get values for the file header
    title = show["name"].replace("&", "&amp;")
    link = show["external_urls"]["spotify"]
    language = show["languages"][0]
    copyright_ = ""
    if show["copyrights"]:
        copyright_ = show["copyrights"][0]
    itunes_author = show["publisher"]
    description = show["description"].replace("&", "&amp;")
    image = show["images"][0]["url"]
    explicit = show["explicit"]
    
    values = (title, link, language, copyright_, itunes_author, description, image, explicit)
    
    #Fill in values
    RSS = head % values
    
    #Generate episodes
    for e in episodes:
        title = e["name"].replace("&", "&amp;")
        url = stock_mp3
        description = e["description"] + "\n\nThis podcast is only available on Spotify. To listen to this episode go to: " + e["external_urls"]["spotify"]
        description = description.replace("&", "&amp;")
        link = e["external_urls"]["spotify"]
        explicit = e["explicit"]
        guid = e["uri"]
        
        if e["release_date_precision"] == "day":
            from datetime import datetime
            date = datetime.strptime(e["release_date"], "%Y-%m-%d")
            date_str = date.strftime("%a, %d %b %Y %H:%M:%S %Z")
        else:
            date_str = "Wed, 29 Sep 2021 05:00:50 GMT"
        
        values = (title, url, description, link, explicit, guid, date_str)
        RSS += ep_template % values
    
    #Add foot
    RSS += foot
    
    uRSS = RSS.encode('utf-8', 'ignore')
    
    return uRSS

def makeRSSShow(show):
    #Get values for the file header
    title = show["name"].replace("&", "&amp;")
    link = show["external_urls"]["spotify"]
    language = show["languages"][0]
    copyright_ = ""
    if show["copyrights"]:
        copyright_ = show["copyrights"][0]
    itunes_author = show["publisher"]
    description = show["description"].replace("&", "&amp;")
    image = show["images"][0]["url"]
    explicit = show["explicit"]
    
    values = (title, link, language, copyright_, itunes_author, description, image, explicit)
    
    #Fill in values
    RSS = head % values
    
    uRSS = RSS.encode('utf-8', 'ignore')
    return uRSS

def makeRSSEpisodes(episodes, isEnd=False):
    RSS = ""
    #Generate episodes
    for e in episodes:
        title = e["name"].replace("&", "&amp;")
        url = stock_mp3
        description = e["description"] + "\n\nThis podcast is only available on Spotify. To listen to this episode go to: " + e["external_urls"]["spotify"]
        description = description.replace("&", "&amp;")
        link = e["external_urls"]["spotify"]
        explicit = e["explicit"]
        guid = e["uri"]
        
        if e["release_date_precision"] == "day":
            from datetime import datetime
            date = datetime.strptime(e["release_date"], "%Y-%m-%d")
            date_str = date.strftime("%a, %d %b %Y %H:%M:%S %Z")
        else:
            date_str = "Wed, 29 Sep 2021 05:00:50 GMT"
        
        values = (title, url, description, link, explicit, guid, date_str)
        RSS += ep_template % values
    
    if isEnd:
        #Add foot
        RSS += foot
    
    uRSS = RSS.encode('utf-8', 'ignore')
    return uRSS