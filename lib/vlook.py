from lxml import etree
from StringIO import StringIO
import re
import requests
import urlparse
import urllib
from lib.site import Site, VideoNotFound

class Vlook(Site):
    def __init__(self):
        pass

    def get_link(self, url):
        r = requests.get(url)
        result = r.text
        patt = re.compile(r'player_src=([^"]*)"')
        match = patt.search(result)
        if not match:
            raise VideoNotFound(url)

        src = urllib.unquote(match.group(1))
        r = requests.head(src)
        vid_link = r.headers["Location"]

        patt = re.compile(r'player_poster=([^&]*)&')
        match = patt.search(result)
        img_link = ''
        if match:
            img_link = urllib.unquote(match.group(1))
        return {"vid": vid_link, "img": img_link}

if __name__ == "__main__":
    site = Vlook()
    print site.get_link('http://www.vlook.cn/show/qs/YklkPTI4OTgwMzc=')

