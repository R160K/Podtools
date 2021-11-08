#api.common

from general import hooker

@hooker("api", "urlHooks", "url_hook")
def set_up_url_hooks():
    pass