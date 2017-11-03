# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from web import views

urlpatterns = [
    url(r'^dimension_action/$', views.DimensionAction.as_view()),
    url(r'^dimension_detail/$', views.DimensionDetail.as_view()),
    url(r'^dimension_list/$', views.DimensionList.as_view()),

    url(r'^attribute_action/$', views.AttributeAction.as_view()),
    url(r'^attribute_detail/$', views.AttributeDetail.as_view()),
    url(r'^attribute_list/$', views.AttributeList.as_view()),

    url(r'^tag_action/$', views.TagAction.as_view()),
    url(r'^tag_detail/$', views.TagDetail.as_view()),
    url(r'^tag_list/$', views.TagList.as_view()),

    url(r'^tag_configure_action/$', views.TagConfigureAction.as_view()),
    url(r'^tag_configure_detail/$', views.TagConfigureDetail.as_view()),
    url(r'^tag_configure_list/$', views.TagConfigureList.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)


