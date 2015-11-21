from lxml import etree
from StringIO import StringIO
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound

class Meipai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//div[@id="detailVideo"]/@data-video')
        if len(links) == 0:
            raise VideoNotFound(url)
        vid_link = links[0]

        img_links = tree.xpath('//div[@id="detailVideo"]/img/@src')
        img_link = ''
        if len(img_links) > 0:
            img_link = img_links[0]

        descs = tree.xpath('//h1[@class="detail-description break"]/text()')
        desc = " ".join(descs)
        return {"vid": vid_link, "img": img_link, "desc": desc}

if __name__ == "__main__":
    meipai = Meipai()
    print meipai.get_link('http://www.meipai.com/media/435782479')

