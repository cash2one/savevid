from lxml import etree
import requests

class VideoNotFound(Exception):
    pass
class NoSearchResults(Exception):
    pass
class NotImplemented(Exception):
    pass

def get_inner_html(elem):
    return "".join([ etree.tostring(e) for e in elem.getchildren() ])

def get_orig_url(url):
    r = requests.head(url, timeout=5)
    return r.headers["Location"]

class Site:
    def __init__(self):
        pass

    def get_link(self, url):
        raise NotImplemented()

