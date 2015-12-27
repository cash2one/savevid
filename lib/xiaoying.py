from lxml import etree
from StringIO import StringIO
import re
import json
import urlparse
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Xiaoying(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        parsed = urlparse.urlsplit(url)
        patt = re.compile(r"/v/([^/]*)/")
        match = patt.search(parsed.path)
        if not match:
            raise VideoNotFound()

        puid = match.group(1)
        img_url = 'http://w.api.xiaoying.co/webapi2/rest/video/publishinfo.get?callback=videocallbackinfo&appkey=30000000&puid=%s' % (puid)
        vid_url = 'http://w.api.xiaoying.co/webapi2/rest/video/videourl?callback=videocallbackvideosrc&appkey=30000000&puid=%s' % (puid)

        r = requests.get(img_url, timeout=10)
        result = r.text
        patt = re.compile(r"\((\{.*\})\)")
        match = patt.search(result)
        img_link = ""
        if match:
            data = json.loads(match.group(1))
            img_link = data["videoinfo"]["coverurl"]

        r = requests.get(vid_url, timeout=10)
        result = r.text
        match = patt.search(result)
        if not match:
            raise VideoNotFound()
        data = json.loads(match.group(1))
        vid_link = data["url"]

        desc = ""
        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=xiaoying.tv&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
        try:
            r = requests.get(url, timeout=10)
        except Exception, e:
            return []
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

    def __search_mp4(self, tree):
        divs = tree.xpath('//div[@class="vid_img"]')
        if len(divs) == 0:
            raise VideoNotFound()

        vid_link = divs[0].get('data-url')
        img_links = divs[0].find('.//img')
        img_link = ""
        try:
            img_link = img_links.get('src')
        except:
            pass
        return {"vid": vid_link, "img": img_link, "desc": ""}

if __name__ == "__main__":
    site = Xiaoying()
    print site.get_link('http://xiaoying.tv/v/lj3mm/1/')
    print site.search_video('hello', 1, 2)

