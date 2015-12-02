import urlparse
import miaopai, weipai, meipai, weibo, vlook
class SiteNotSupported(Exception):
    pass

class SiteFactory:
    def __init__(self, url):
        self.url = url
        parsed = urlparse.urlsplit(url)
        netloc = parsed.netloc
        self.site = None
        if netloc == "video.weibo.com":
            self.site = weibo.Weibo()
        elif netloc == "www.meipai.com":
            self.site = meipai.Meipai()
        elif netloc == "www.miaopai.com":
            self.site = miaopai.Miaopai()
        elif netloc == "www.weipai.cn":
            self.site = weipai.Weipai()
        elif netloc == "www.vlook.cn":
            self.site = vlook.Vlook()
        else:
            raise SiteNotSupported()

    def get_link(self):
        return self.site.get_link(self.url)
