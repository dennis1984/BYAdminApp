# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from web import views

urlpatterns = [
    # 维度
    url(r'^dimension_action/$', views.DimensionAction.as_view()),
    url(r'^dimension_detail/$', views.DimensionDetail.as_view()),
    url(r'^dimension_list/$', views.DimensionList.as_view()),

    # 属性
    url(r'^attribute_action/$', views.AttributeAction.as_view()),
    url(r'^attribute_detail/$', views.AttributeDetail.as_view()),
    url(r'^attribute_list/$', views.AttributeList.as_view()),

    # 标签
    url(r'^tag_action/$', views.TagAction.as_view()),
    url(r'^tag_detail/$', views.TagDetail.as_view()),
    url(r'^tag_list/$', views.TagList.as_view()),

    # 标签配置
    url(r'^tag_configure_action/$', views.TagConfigureAction.as_view()),
    url(r'^tag_configure_detail/$', views.TagConfigureDetail.as_view()),
    url(r'^tag_configure_list/$', views.TagConfigureList.as_view()),

    # 资源类型
    url(r'^media_type_action/$', views.MediaTypeAction.as_view()),
    url(r'^media_type_detail/$', views.MediaTypeDetail.as_view()),
    url(r'^media_type_list/$', views.MediaTypeList.as_view()),

    # 题材类型
    url(r'^theme_type_action/$', views.ThemeTypeAction.as_view()),
    url(r'^theme_type_detail/$', views.ThemeTypeDetail.as_view()),
    url(r'^theme_type_list/$', views.ThemeTypeList.as_view()),

    # 项目进度
    url(r'^project_progress_action/$', views.ProjectProgressAction.as_view()),
    url(r'^project_progress_detail/$', views.ProjectProgressDetail.as_view()),
    url(r'^project_progress_list/$', views.ProjectProgressList.as_view()),

    # 媒体资源
    url(r'^media_action/$', views.MediaAction.as_view()),
    url(r'^media_detail/$', views.MediaDetail.as_view()),
    url(r'^media_list/$', views.MediaList.as_view()),

    # 媒体资源配置
    url(r'^media_configure_action/$', views.MediaConfigureAction.as_view()),
    url(r'^media_configure_detail/$', views.MediaConfigureDetail.as_view()),
    url(r'^media_configure_list/$', views.MediaConfigureList.as_view()),

    # 资源标签
    url(r'^resource_tag_action/$', views.ResourceTagAction.as_view()),
    url(r'^resource_tag_detail/$', views.ResourceTagDetail.as_view()),
    url(r'^resource_tag_list/$', views.ResourceTagList.as_view()),

    # 报告文件
    url(r'^report_action/$', views.ReportAction.as_view()),
    url(r'^report_detail/$', views.ReportDetail.as_view()),
    url(r'^report_list/$', views.ReportList.as_view()),

    # 用户评论及管理员回复
    url(r'^reply_comment_action/$', views.ReplyCommentAction.as_view()),
    url(r'^comment_and_reply_detail/$', views.CommentAndReplyDetail.as_view()),
    url(r'^comment_and_reply_list/$', views.CommentAndReplyList.as_view()),

    # 资讯
    url(r'^information_action/$', views.InformationAction.as_view()),
    url(r'^information_detail/$', views.InformationDetail.as_view()),
    url(r'^information_list/$', views.InformationList.as_view()),

    # 案例
    url(r'^case_action/$', views.CaseAction.as_view()),
    url(r'^case_detail/$', views.CaseDetail.as_view()),
    url(r'^case_list/$', views.CaseList.as_view()),

    # 用户角色
    url(r'^user_role_action/$', views.UserRoleAction.as_view()),
    url(r'^user_role_detail/$', views.UserRoleDetail.as_view()),
    url(r'^user_role_list/$', views.UserRoleList.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)


