from lxml import etree
from StringIO import StringIO
import re
import requests
import urlparse
import urllib
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Vlook(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=5)
        result = r.text
        patt = re.compile(r'player_src=([^"]*)"')
        match = patt.search(result)
        if not match:
            raise VideoNotFound(url)

        src = urllib.unquote(match.group(1))
        vid_link = get_orig_url(src)

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

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=vlook.cn&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
        r = requests.get(url, timeout=5)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        divs = tree.xpath('//div[@id="content_left"]/div[@id]')
        results = []
        for div in divs:
            a_node = div.find('.//h3/a')
            title = get_inner_html(a_node)
            vid_link = get_orig_url(a_node.get('href'))
            img_node = div.find('.//div/div/a/img')
            img_link = ""
            if img_node:
                img_link = img_node.get('src')
            desc = get_inner_html(div.find('.//div[@class="c-abstract"]'))
            results.append({"title": title,
                "vid": vid_link,
                "img": img_link,
                "desc": desc})
        return results

if __name__ == "__main__":
    site = Vlook()
    print site.get_link('http://www.vlook.cn/show/qs/YklkPTI4OTgwMzc=')
    print site.search_video('hello', 1, 2)

