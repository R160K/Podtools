#api.rss_finder.plugins.common

from general import hooker

@hooker("api.rss_finder", "queryHooks", "query_hook")
def set_up_query_hooks():
    pass