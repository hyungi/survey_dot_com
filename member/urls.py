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
from member import views

urlpatterns = [
    url(r'^info/$', views.member_info, name='member_info'),
    url(r'^edit/$', views.member_edit, name='member_edit'),
    url(r'^(?P<pk>\d+)/sign_out/$', views.sign_out, name='sign_out'),
]
'''
member
pk 노출 하지 않기
(?P<pk>\d+)/주어/동사_목적어
'''

# url(r'^group/$', views.all_group_list, name='all_group_list'),
# url(r'^group/(?P<pk>\d+)/$', views.my_group_list, name='my_group_list'),
# url(r'^group/my/(?P<pk>\d+)/$', views.my_group_detail, name='my_group_detail'),
# url(r'^group/my/(?P<pk>\d+)/edit/$', views.group_edit, name='group_edit'),
# url(r'^group/new', views.new_group, name='new_group'),
# url(r'^group/apply/(?P<pk>\d+)/$', views.apply_group, name='apply_group'),
