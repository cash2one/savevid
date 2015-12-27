import re
import urlparse
import lib.site
import miaopai
import weipai
import meipai
import weibo
import vlook
import weipainv
import xiaoying
import xiaokaxiu
import gifshow
import v1
import tumblr
import mitaose

class SiteNotSupported(Exception):
    pass

site_class = {"weibo": weibo.Weibo,
    "miaopai": miaopai.Miaopai,
    "weipai": weipai.Weipai,
    "meipai": meipai.Meipai,
    "vlook": vlook.Vlook,
    "weipainv": weipainv.Weipainv,
    "xiaoying": xiaoying.Xiaoying,
    "xiaokaxiu": xiaokaxiu.Xiaokaxiu,
    "gifshow": gifshow.Gifshow,
    "v1": v1.V1,
    "tumblr": tumblr.Tumblr,
    "mitaose": mitaose.Mitaose,
    }

class SiteFactory:
    def __init__(self, name=None, url=None):
        if name:
            if not site_class.has_key(name):
                raise SiteNotSupported()

            site = site_class[name]
            self.site = site()
        else:
            try:
                self.url = lib.site.get_orig_url(url)
            except:
                self.url = url
            parsed = urlparse.urlsplit(self.url)
            netloc = parsed.netloc
            self.site = None
            if re.search(r"weibo.com|weibo.cn|sinajs.cn|sinaimg.cn", netloc):
                self.site = weibo.Weibo()
            elif re.search(r"meipai.com", netloc):
                self.site = meipai.Meipai()
            elif re.search(r"miaopai.com|ent.v.sina.cn", netloc):
                self.site = miaopai.Miaopai()
            elif re.search(r"weipai.cn", netloc):
                self.site = weipai.Weipai()
            elif re.search(r"vlook.cn", netloc):
                self.site = vlook.Vlook()
            elif re.search(r"weipainv.com", netloc):
                self.site = weipainv.Weipainv()
            elif re.search(r"xiaoying.tv", netloc):
                self.site = xiaoying.Xiaoying()
            elif re.search(r"xiaokaxiu.com", netloc):
                self.site = xiaokaxiu.Xiaokaxiu()
            elif re.search(r"gifshow.com|kuaishou.com", netloc):
                self.site = gifshow.Gifshow()
            elif re.search(r"v1.cn", netloc):
                self.site = v1.V1()
            elif re.search(r"tumblr.com", netloc):
                self.site = tumblr.Tumblr()
            elif re.search(r"mitaose8.com", netloc):
                self.site = mitaose.Mitaose()
            else:
                raise SiteNotSupported()

    def get_link(self):
        return self.site.get_link(self.url)

    def search_video(self, keyword, page_num, num_per_page):
        return self.site.search_video(keyword, page_num, num_per_page)
