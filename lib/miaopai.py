from lxml import etree
from StringIO import StringIO
import re
import requests
from lib.site import Site, VideoNotFound

class Miaopai(Site):
    def __init__(self):
        pass

    def get_link(self, url):
        r = requests.get(url)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//param[@name="src"]/@value')

        if len(links) > 0:
            link = links[0]
            patt = re.compile(r"\?scid=(.*?)&")
            match = patt.search(link)
            if match:
                scid = match.group(1)
                link = "http://gslb.miaopai.com/stream/%s.mp4" % (scid)
            return link
        raise VideoNotFound(url)

if __name__ == "__main__":
    miaopai = Miaopai()
    print miaopai.get_link('http://www.miaopai.com/show/fEhYvm~vakOc22cw~n8rJg__.htm')
