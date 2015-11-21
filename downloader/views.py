from django.shortcuts import render
from django.http import JsonResponse
import re
from lib import *
import urlparse

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
        return JsonResponse({"success": True, "msg": "video not found"})

    try:
        data = site.get_link(url)
    except:
        return JsonResponse({"success": False, "msg": "failed to get download link"})
    return JsonResponse({"success": True, "msg": "", "result": data})
