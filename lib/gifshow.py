from lxml import etree
from StringIO import StringIO
import logging
import re
import requests
import urlparse
import urllib
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

logger = logging.getLogger(__name__)

class Gifshow(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=10)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//video[@id="myvid"]')

        if len(links) == 0:
            raise VideoNotFound(url)
        vid_link = links[0].get('src')

        img_link = links[0].get('poster')
        desc = ""
        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=kuaishou.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
        r = requests.get(url, timeout=10)
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
    site = Gifshow()
    print site.get_link('http://www.kuaishou.com/i/photo/lwx?userId=87061162&photoId=478026608&cc=share_copylink&fid=43890132&et=1_i%2F1519425450749902849_f0')
    print site.get_link('http://www.gifshow.com/i/photo/lwx?userId=87061162&photoId=478026608&cc=share_copylink&fid=43890132&et=1_i%2F1519425450749902849_f0')
    print site.search_video('hello', 1, 2)

