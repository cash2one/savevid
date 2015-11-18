from django.shortcuts import render
from django.http import JsonResponse
import re
import lib
import urlparse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def get_link(request):
    data = request.POST.get("url", "")
    if data == "":
        return JsonResponse({"success": True, "msg": "empty url"})
    parsed = urlparse.urlsplit(data)
    netloc = parsed.netloc
    site = None
    if netloc == "video.weibo.com":
        site = lib.weibo.Weibo()
    elif netloc == "www.meipai.com":
        site = lib.meipai.Meipai()
    elif netloc == "www.miaopai.com":
        site = lib.miaopai.Miaopai()
    elif netloc == "www.weipai.cn":
        site = lib.weipai.Weipai()
    link = site.get_link(data)
    return JsonResponse({"success": True, "msg": ""})
