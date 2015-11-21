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
        r = requests.get(url, timeout=5)
        result = r.text
        patt = re.compile(r'player_src=([^"]*)"')
        match = patt.search(result)
        if not match:
            raise VideoNotFound(url)

        src = urllib.unquote(match.group(1))
        r = requests.head(src, timeout=5)
        vid_link = r.headers["Location"]

        patt = re.compile(r'player_poster=([^&]*)&')
        match = patt.search(result)
        img_link = ''
        if match:
            img_link = urllib.unquote(match.group(1))

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        descs = tree.xpath('//div[@class="detail_des"]')
        desc = ""
        if len(descs) > 0:
            desc = descs[0].text
        return {"vid": vid_link, "img": img_link, "desc": desc}

if __name__ == "__main__":
    site = Vlook()
    print site.get_link('http://www.vlook.cn/show/qs/YklkPTI4OTgwMzc=')

