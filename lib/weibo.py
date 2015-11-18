from lxml import etree
from StringIO import StringIO
import re
import requests
import urlparse
import urllib
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

        flashvars = links[0]
        patt = re.compile(r'list=(.*)')
        match = patt.search(flashvars)
        if not match:
            raise VideoNotFound()
        link = urllib.unquote(match.group(1))
        path = self.extract_mp4(link)
        netloc = urlparse.urlsplit(link).netloc
        vid_url = "http://%s/%s" % (netloc, path)
        return vid_url

    def extract_mp4(self, url):
        r = requests.get(url)
        result = r.text
        lines = result.split("\n")
        patt = re.compile(r'^#')
        lines = filter(lambda x: not patt.match(x), lines)
        if len(lines) == 0:
            raise VideoNotFound()

        return lines[0]

if __name__ == "__main__":
    weibo = Weibo()
#    print weibo.get_link('http://video.weibo.com/player/1034:172d8e9a6a92e9d530f730e8a3dc1587/v.swf')
    print weibo.get_link('http://video.weibo.com/show?fid=1034:fbc31906b81fc46b1408757ea8d5c8d2')
