from lxml import etree
from StringIO import StringIO
import re
import requests
from lib.site import Site, VideoNotFound

class Weibo(Site):
    def __init__(self):
        pass

    def get_link(self, url):
        r = requests.get(url)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//embed/@flashvars')

        if len(links) == 0:
            raise VideoNotFound()

        link = links[0]
        print link
        patt = re.compile(r"\?scid=(.*?)&")
        match = patt.search(link)
        if match:
            scid = match.group(1)
            link = "http://gslb.miaopai.com/stream/%s.mp4" % (scid)
        return link

if __name__ == "__main__":
    weibo = Weibo()
    print weibo.get_link('http://video.weibo.com/player/1034:172d8e9a6a92e9d530f730e8a3dc1587/v.swf')
    print weibo.get_link('http://video.weibo.com/show?fid=1034:82947d751e791d064c2db09cd9c6c97b')
