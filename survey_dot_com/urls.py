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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html'), name='profile'),
    # url(r'^$', views.Home.as_view(), name='home'),

    url(r'^member/', include('member.urls')),
    url(r'^survey/', include('survey.urls')),
    url(r'^draft/', include('draft.urls')),

    # url(r'^member/info/$', views.member_info, name='member_info'),
    # url(r'^member/edit/$', views.member_info_edit, name='member_info_edit'),
    # url(r'^member/(?P<pk>\d+)/sign_out/$', views.sign_out, name='sign_out'),
    #
    # url(r'^survey/$', views.all_survey_list, name='all_survey'),
    # url(r'^survey/my_list/$', views.my_survey_list, name='my_survey_list'),
    # url(r'^survey/show/(?P<pk>\d+)/$', views.show_survey, name='show_survey'),
    # url(r'^survey/my/(?P<pk>\d+)/delete/$', views.del_survey, name='del_survey'),
    # url(r'^survey/my/(?P<pk>\d+)/edit/$', views.edit_survey, name='edit_survey'),
    # url(r'^survey/new', views.new_survey, name='new_survey'),
    #
    # url(r'^draft/my_list/$', views.my_draft_list, name='my_draft_list'),
    # url(r'^draft/show/(?P<pk>\d+)/$', views.my_draft_detail, name='show_draft'),
    # url(r'^draft/my/(?P<pk>\d+)/delete/$', views.del_draft, name='del_draft'),
    # url(r'^draft/my/(?P<pk>\d+)/edit/$', views.edit_draft, name='edit_draft'),
    # url(r'^draft/new', views.new_draft, name='new_draft'),

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
