#api.spotify_tools.rss_builder
import engine.signal as signal

HEAD_HREF = "./api/spotify_tools/rss_templates/head.rss"
FOOT_HREF = "./api/spotify_tools/rss_templates/foot.rss"
EP_TEMPLATE_HREF = "./api/spotify_tools/rss_templates/episode.rss"

head = signal.ValueLoader(HEAD_HREF)
foot = signal.ValueLoader(FOOT_HREF)
ep_template = signal.ValueLoader(EP_TEMPLATE_HREF)

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
    RSS = head.content % values
    
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
        RSS += ep_template.content % values
    
    #Add foot
    RSS += foot.content
    
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
    itunes_author = show["publisher"].replace("&", "&amp;")
    description = show["description"].replace("&", "&amp;")
    image = show["images"][0]["url"]
    explicit = show["explicit"]
    
    values = (title, link, language, copyright_, itunes_author, description, image, explicit)
    
    #Fill in values
    RSS = head.content % values
    
    uRSS = RSS.encode('utf-8', 'ignore')
    return uRSS

def makeRSSEpisodes(episodes, isEnd=False):
    RSS = ""
    #Generate episodes
    for e in episodes:
        title = e["name"].replace("&", "&amp;")
        url = stock_mp3
        description = e["description"] + "\n\nThis podcast is only available on Spotify. To listen to this episode go to: " + e["external_urls"]["spotify"]
        # description = description.replace("&", "&amp;")
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
        RSS += ep_template.content % values
    
    if isEnd:
        #Add foot
        RSS += foot.content
    
    uRSS = RSS.encode('utf-8', 'ignore')
    return uRSS