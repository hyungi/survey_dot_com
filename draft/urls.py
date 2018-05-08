"""survey_dot_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from draft import views

urlpatterns = [
    url(r'^my_list/$', views.my_draft_list, name='my_draft_list'),
    url(r'^show/(?P<pk>\d+)/$', views.my_draft, name='my_draft'),
    url(r'^my/(?P<pk>\d+)/delete/$', views.del_draft, name='del_draft'),
    url(r'^my/(?P<pk>\d+)/edit/$', views.edit_draft, name='edit_draft'),
    url(r'^new', views.new_draft, name='new_draft'),
    url(r'^search/$', views.search_draft, name='search_draft'),
]
'''
member
pk 노출 하지 않기
(?P<pk>\d+)/주어/동사_목적어
'''