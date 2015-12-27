from lxml import etree
from StringIO import StringIO
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Tumblr(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=10)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//iframe[@src]')
        if len(links) == 0:
            raise VideoNotFound(url)
        vid_link = links[0].get("src")

        r = requests.get(vid_link, timeout=10)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//source[@src]')
        if len(links) == 0:
            raise VideoNotFound(url)
        vid_link = links[0].get("src")
        vid_link = get_orig_url(vid_link)
        img_links = tree.xpath('//video[@poster]')
        img_link = ''
        if len(img_links) > 0:
            img_link = img_links[0].get("poster")
        desc = ""
        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=tumblr.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
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
    meipai = Tumblr()
    print meipai.get_link('http://loliuu.tumblr.com/post/135382574742')
    print meipai.search_video('hello', 1, 2)

