#-*- coding:utf-8 -*-
import logging
import re
import urlparse
import Queue
import threading
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from lib import *

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

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
        return JsonResponse({"success": False, "msg": u"暂不支持该网站视频下载，我们会尽快添加"})

    try:
        data = site.get_link(url)
    except:
        logger.error("cannot get video link for %s" % (url))
        return JsonResponse({"success": False, "msg": u"获取下载地址失败了:(，我们正在全力查找原因..."})
    logger.debug("got video link for %s" % (url))
    return JsonResponse({"success": True, "msg": "", "result": data})

def search_vid(request):
    def worker(q, keyword, page_num, results):
        while not q.empty():
            site_class = q.get()
            site = site_class()
            site_results = site.search_video(keyword, page_num, 10)
            results.extend(site_results)
            q.task_done()

    keyword = request.POST.get("keyword", "")
    page_num = request.GET.get("pn", 1)
    page_num = int(page_num)
    site_classes = [weibo.Weibo, meipai.Meipai, miaopai.Miaopai, weipai.Weipai, vlook.Vlook]
    results = []
    q = Queue.Queue()
    for site_class in site_classes:
        q.put(site_class)
        thr = threading.Thread(target=worker, args=(q, keyword, page_num, results))
        thr.setDaemon(True)
        thr.start()
    q.join()
    results = filter(lambda x: x["img"], results)
    if len(results) == 0:
        return JsonResponse({"success": False, "msg": u"没有找到视频:("})
    return JsonResponse({"success": True, "msg": "", "result": results})

def aboutus(request):
    return render(request, 'aboutus.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def login(request):
    if request.method == "GET":
        raise Http404("Invalid Request")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if not request.POST.get("remember_me", None):
                request.session.set_expiry(0)
            auth.login(request, user)
            return JsonResponse({"success": True, "msg": ""})
        else:
            err = "Invalid username or password"
            return JsonResponse({"success": False, "msg": err})

def userlogin(request):
    return render(request, "login.html")

def userregister(request):
    return render(request, "register.html")

def register(request):
    return render(request, "register.html")

def logout(request):
    auth.logout(request)
    return redirect("index")

