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
        text = text + get_inner_html(e)

    if elem.tail is not None:
        text = text + elem.tail
    return text

def get_orig_url(url):
    r = requests.get(url, timeout=10, allow_redirects=False)
    if "Location" in r.headers:
        return r.headers["Location"]
    r = requests.get(url, timeout=10)
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

if __name__ == "__main__":
    print get_orig_url("http://service.vlook.cn:8080/down/servlet/VideoPlay?vid=cANr&client=pc&imei=f8e36ddffcb7fca735ed7bfeeb1345fb")
    print get_orig_url("http://www.baidu.com")
