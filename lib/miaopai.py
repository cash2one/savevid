from lxml import etree
from StringIO import StringIO
import re
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Miaopai(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=10)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//param[@name="src"]/@value')

        if len(links) == 0:
            return self.__search_mp4(tree)

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

        descs = tree.xpath('//div[@class="introduction"]/p')
        desc = ''
        if len(descs) > 0:
            desc = descs[0].text

        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=miaopai.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
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
    miaopai = Miaopai()
    print miaopai.get_link('http://www.miaopai.com/show/fEhYvm~vakOc22cw~n8rJg__.htm')
    print miaopai.search_video('hello', 1, 2)
    print miaopai.get_link('http://m.miaopai.com/v2_index/topic/WREKRDEoIMBjKczu')
