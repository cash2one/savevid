from lxml import etree
from StringIO import StringIO
import re
import base64
import requests
import urlparse
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Weipai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=10)
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
        r = requests.get(share_link, timeout=10)
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

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=weipai.cn&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        divs = tree.xpath('//div[@id="content_left"]/div[@class="result c-container "]')
        results = []
        for div in divs:
            a_node = div.find('.//h3/a')
            title = get_inner_html(a_node)
            vid_link = get_orig_url(a_node.get('href'))
            img_node = div.find('.//div/div/a/img')
            img_link = ""
            if img_node is not None:
                img_link = img_node.get('src')
            descs = div.iterfind('.//div[@class="c-abstract"]')
            desc = ""
            try:
                desc_elem = descs.next()
                desc = get_inner_html(desc_elem)
            except:
                pass
            results.append({"title": title,
                "vid": vid_link,
                "img": img_link,
                "desc": desc})
        return results

if __name__ == "__main__":
    weipai = Weipai()
    print weipai.get_link('http://www.weipai.cn/video/5558b72c2296013b008b4567')
    print weipai.search_video('hello', 1, 2)
