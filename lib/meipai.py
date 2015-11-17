from lxml import etree
from StringIO import StringIO
import requests
from lib.site import Site, VideoNotFound

class Meipai(Site):
    def __init__(self):
        pass

    def get_link(self, url):
        r = requests.get(url)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//div[@id="detailVideo"]/@data-video')
        if len(links) > 0:
            link = links[0]
            return link
        raise VideoNotFound(url)

if __name__ == "__main__":
    meipai = Meipai()
    print meipai.get_link('http://www.meipai.com/media/435782479')

