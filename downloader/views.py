#-*- coding:utf-8 -*-
import logging
import re
import urlparse
from django.shortcuts import render
from django.http import JsonResponse
from lib import *

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def get_link(request):
    url = request.POST.get("url", "")
    if url == "":
        return JsonResponse({"success": True, "msg": "empty url"})
    parsed = urlparse.urlsplit(url)
    netloc = parsed.netloc
    site = None
    if netloc == "video.weibo.com":
        site = weibo.Weibo()
    elif netloc == "www.meipai.com":
        site = meipai.Meipai()
    elif netloc == "www.miaopai.com":
        site = miaopai.Miaopai()
    elif netloc == "www.weipai.cn":
        site = weipai.Weipai()
    elif netloc == "www.vlook.cn":
        site = vlook.Vlook()
    else:
        return JsonResponse({"success": False, "msg": u"目前暂不支持该网站的视频下载: " + netloc})

    try:
        data = site.get_link(url)
    except:
        logger.error("cannot get video link for %s" % (url))
        return JsonResponse({"success": False, "msg": u"获取下载地址失败"})
    logger.debug("got video link for %s" % (url))
    return JsonResponse({"success": True, "msg": "", "result": data})

def aboutus(request):
    return render(request, 'aboutus.html')
