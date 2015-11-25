from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_vid/$', views.search_vid, name='search_vid'),
    url(r'^get_link/$', views.get_link, name='get_link'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^tutorial/$', views.tutorial, name='tutorial'),
#    url(r'^userlogin/$', views.userlogin, name='userlogin'),
#    url(r'^logout/$', views.logout, name='logout'),
#    url(r'^login/$', views.login, name='login'),
#    url(r'^register/$', views.register, name='register'),
#    url(r'^userregister/$', views.userregister, name='userregister'),
]
