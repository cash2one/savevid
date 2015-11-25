from lxml import etree
from StringIO import StringIO
import re
import requests
import urlparse
import urllib
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Weibo(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=5)
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
        path = self.__extract_mp4(link)
        netloc = urlparse.urlsplit(link).netloc
        vid_link = "http://%s/%s" % (netloc, path)
        img_links = tree.xpath('//img/@src')
        img_link = ''
        if len(img_links) > 0:
            img_link = img_links[0]
        return {"vid": vid_link, "img": img_link, "desc": ""}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=video.weibo.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
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

    def __extract_mp4(self, url):
        r = requests.get(url, timeout=5)
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
    print weibo.search_video('hello', 1, 2)
