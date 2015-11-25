#-*- coding:utf-8 -*-
import re
from lxml import etree
from StringIO import StringIO
import requests

class VideoNotFound(Exception):
    pass
class NoSearchResults(Exception):
    pass
class OrigUrlNotFound(Exception):
    pass
class NotImplemented(Exception):
    pass

def get_inner_html(elem):
    text = elem.text
    if text is None:
        text = ""

    for e in elem.getchildren():
        text = text + etree.tostring(e, encoding='UTF-8')
    return text

def get_orig_url(url):
    r = requests.get(url, timeout=5)
    if "Location" in r.headers:
        return r.headers["Location"]
    result = r.text
    patt = re.compile(r'window.location.replace\("(.*)"')
    match = patt.search(result)
    if match:
        return match.group(1)
    raise OrigUrlNotFound(url)

class Site:
    def __init__(self):
        pass

    def get_link(self, url):
        raise NotImplemented()

