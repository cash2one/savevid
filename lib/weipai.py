from lxml import etree
from StringIO import StringIO
import re
import base64
import requests
import urlparse
from lib.timeit import timeit
from lib.site import Site, VideoNotFound

class Weipai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//div[@class="video_player"]/a[@class="play"]/@onclick')
        #result = etree.tostring(tree.getroot(),
        #    pretty_print=True, method="html")
        #print result
        if len(links) == 0:
            raise VideoNotFound(url)
        link = links[0]
        patt = re.compile(r"playVideo\('(.*?)'")
        match = patt.search(link)
        if not match:
            raise VideoNotFound(url)

        vid = match.group(1)
        share_link = 'http://share.weipai.cn/video/play/id/%s/type/theater/source/undefine' % (vid)
        r = requests.get(share_link, timeout=5)
        result = r.text
        patt = re.compile(r"'(http.*?)'")
        match_url = patt.search(result)
        if not match_url:
            raise VideoNotFound(url)

        wrapper_url = match_url.group(1)
        wrapper_params = urlparse.urlsplit(wrapper_url)
        codes = urlparse.parse_qs(wrapper_params.query)['s']
        if len(codes) == 0:
            raise VideoNotFound()
        code = codes[0]
        vid_params = base64.b64decode(code)
        links = urlparse.parse_qs(vid_params)['p']
        if len(links) == 0:
            raise VideoNotFound()
        vid_link = links[0]

        img_links = tree.xpath('//div[@class="video_player"]/div/span/img/@src')
        img_link = 0
        if len(img_links) > 0:
            img_link = img_links[0]
        return {"vid": vid_link, "img": img_link, "desc": ""}

if __name__ == "__main__":
    weipai = Weipai()
    print weipai.get_link('http://www.weipai.cn/video/5558b72c2296013b008b4567')
