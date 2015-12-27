from lxml import etree
from StringIO import StringIO
import re
import requests
from lib.timeit import timeit
from lib.site import Site, VideoNotFound, get_inner_html, get_orig_url

class Weipainv(Site):
    def __init__(self):
        pass

    @timeit
    def get_link(self, url):
        r = requests.get(url, timeout=10)
        result = r.text
        #print result.encode("utf-8")
        patt = re.compile(r'jwplayer\(".*"\).setup\(\{(.*?)\}\)', re.M|re.S)
        match = patt.search(result)
        if not match:
            raise VideoNotFound()

        try:
            content = match.group(1)
            patt = re.compile(r'file: "(.*?)".*image: "(.*?)"', re.M|re.S)
            link = patt.search(content)
            vid_link = link.group(1)
            img_link = link.group(2)
            desc = ''
            return {"vid": vid_link, "img": img_link, "desc": desc}
        except:
            raise VideoNotFound()

    @timeit
    def search_video(self, keyword, page_num, num_per_page):
        start = (page_num-1) * num_per_page
        url = "http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&lm=0&ft=&q5=&q6=weipainv.com&tn=baiduadv&pn=%d&rn=%d" % (keyword, start, num_per_page)
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
    site = Weipainv()
    print site.get_link('http://www.weipainv.com/plugin.php?id=smart_video:smart_video&mod=v&tid=487')
    print site.search_video('hello', 1, 2)

