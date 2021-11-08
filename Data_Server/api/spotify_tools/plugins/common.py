#api.spotify_tools.plugins.common

from general import hooker

@hooker("api.spotify_tools", "urlHooks", "url_hook")
def set_up_url_hooks():
    pass