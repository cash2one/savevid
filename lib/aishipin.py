from lxml import etree
from StringIO import StringIO
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url
import re

class Aishipin(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=20)
        result = r.text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(result), parser)
        links = tree.xpath('//div[@id="post_content"]')
        if len(links) == 0:
            raise VideoNotFound(url)

        vid_node = links[0]
        html = etree.tostring(vid_node)
        patt = re.compile(r"setCuSunPlayerVideo\((.*)\)")
        match = patt.search(html)
        if not match:
            return self.get_sinaimg_video(tree)

        params = match.group(1).split(",")
        img_path = params[2]
        img_path = img_path[1:len(img_path)-1]
        img_link = "http://www.aishipin.net" + img_path
        vid_link = params[3]
        vid_link = vid_link[1:len(vid_link)-1]
        p_nodes = vid_node.findall('.//p[@style]')
        desc = get_inner_html(p_nodes[1])
        return {"vid": vid_link, "img": img_link, "desc": desc}

    def get_sinaimg_video(self, tree):
        links = tree.xpath('//source[@src]')
        if len(links) == 0:
            raise VideoNotFound(url)

        vid_link = links[0].get("src")
        img_link = ""
        desc = ""
        return {"vid": vid_link, "img": img_link, "desc": desc}

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=aishipin.net&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
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

if __name__ == "__main__":
    site = Aishipin()
    print site.get_link('http://www.aishipin.net/wpfuli/784.html')
    print site.get_link('http://www.aishipin.net/wpfuli/737.html')
    print site.search_video('hello', 1, 2)

