from lxml import etree
from StringIO import StringIO
import re
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound

class Miaopai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=30)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//param[@name="src"]/@value')

        if len(links) == 0:
            raise VideoNotFound(url)
        link = links[0]
        patt = re.compile(r"\?scid=(.*?)&")
        match = patt.search(link)
        if not match:
            raise VideoNotFound(url)
        scid = match.group(1)
        vid_link = "http://gslb.miaopai.com/stream/%s.mp4" % (scid)
        img_links = tree.xpath('//div[@class="video_img"]/img/@src')
        img_link = ''
        if len(img_links) > 0:
            img_link = img_links[0]

        print scid
        descs = tree.xpath('//div[@class="introduction"]/p')
        desc = ''
        if len(descs) > 0:
            desc = descs[0].text

        return {"vid": vid_link, "img": img_link, "desc": desc}

if __name__ == "__main__":
    miaopai = Miaopai()
    print miaopai.get_link('http://www.miaopai.com/show/fEhYvm~vakOc22cw~n8rJg__.htm')
