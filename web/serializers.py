# -*- coding:utf8 -*-
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.conf import settings

from horizon.models import model_to_dict
from horizon import main
from horizon import forms
from horizon.decorators import has_permission_to_update
from horizon.serializers import (BaseListSerializer,
                                 BaseModelSerializer,
                                 BaseSerializer,
                                 timezoneStringTostring)

from Web_App.web_dimensions.models import (Dimension,
                                           Attribute,
                                           TagConfigure,
                                           Tag,
                                           AdjustCoefficient)
from Web_App.web_media.models import (Media, MediaConfigure,
                                      MediaType, ThemeType,
                                      ProjectProgress,
                                      ResourceTags,
                                      Information, Case,
                                      AdvertResource)
from Web_App.web_reports.models import Report, ReportDownloadRecord
from Web_App.web_comment.models import (Comment, ReplyComment)
from Web_App.web_users.models import Role
from web.caches import BaseCache

import urllib
import os
import json
import re
import copy
import cStringIO


class DimensionSerializer(BaseModelSerializer):
    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            super(DimensionSerializer, self).__init__(data=data, **kwargs)
        else:
            super(DimensionSerializer, self).__init__(instance, **kwargs)

    class Meta:
        model = Dimension
        fields = '__all__'

    def save(self, **kwargs):
        # 删除缓存
        BaseCache().delete_dimension_list()
        return super(DimensionSerializer, self).save(**kwargs)

    def update(self, instance, validated_data):
        # 删除缓存
        BaseCache().delete_dimension_list()

        pop_keys = ['dimension_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(DimensionSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        # 删除缓存
        BaseCache().delete_dimension_list()

        validated_data = {'status': instance.id + 1}
        return super(DimensionSerializer, self).update(instance, validated_data)


class DimensionListSerializer(BaseListSerializer):
    child = DimensionSerializer()


class AttributeSerializer(BaseModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['attribute_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(AttributeSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(AttributeSerializer, self).update(instance, validated_data)


class AttributeDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    dimension_id = serializers.IntegerField()
    dimension_name = serializers.CharField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class AttributeListSerializer(BaseListSerializer):
    child = AttributeDetailSerializer()


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, instance, validated_data):
        self.delete_tag_list_from_cache()
        pop_keys = ['tag_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(TagSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        self.delete_tag_list_from_cache()
        validated_data = {'status': instance.id + 1}
        return super(TagSerializer, self).update(instance, validated_data)

    def delete_tag_list_from_cache(self):
        # 删除缓存
        dimension_instances = Dimension.filter_objects()
        for ins in dimension_instances:
            BaseCache().delete_tag_list_by_dimension_id(dimension_id=ins.id)


class TagListSerializer(BaseListSerializer):
    child = TagSerializer()


class TagConfigureSerializer(BaseModelSerializer):
    class Meta:
        model = TagConfigure
        fields = '__all__'

    def update(self, instance, validated_data):
        self.delete_tag_list_from_cache()
        pop_keys = ['tag_configure_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(TagConfigureSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        self.delete_tag_list_from_cache()
        validated_data = {'status': instance.id + 1}
        return super(TagConfigureSerializer, self).update(instance, validated_data)

    def delete_tag_list_from_cache(self):
        # 删除缓存
        dimension_instances = Dimension.filter_objects()
        for ins in dimension_instances:
            BaseCache().delete_tag_list_by_dimension_id(dimension_id=ins.id)


class TagConfigureDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    tag_id = serializers.IntegerField()
    tag_name = serializers.CharField()
    attribute_id = serializers.IntegerField()
    attribute_name = serializers.CharField()
    match_value = serializers.FloatField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class TagConfigureListSerializer(BaseListSerializer):
    child = TagConfigureDetailSerializer()


MEDIA_IMAGE_PATH = settings.PICTURE_DIRS['web']['media']


class MediaSerializer(BaseModelSerializer):
    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            if 'media_type_id' in data:
                data['media_type'] = data.pop('media_type_id')
            if 'theme_type_id' in data:
                data['theme_type'] = data.pop('theme_type_id')
            if 'progress_id' in data:
                data['progress'] = data.pop('progress_id')
            super(MediaSerializer, self).__init__(data=data, **kwargs)
        else:
            super(MediaSerializer, self).__init__(instance, **kwargs)

    class Meta:
        model = Media
        fields = '__all__'

    def update(self, instance, validated_data):
        # 删除缓存
        BaseCache().delete_media_by_id(media_id=instance.id)

        pop_keys = ['media_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(MediaSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        # 删除缓存
        BaseCache().delete_media_by_id(media_id=instance.id)

        validated_data = {'status': instance.id + 1}
        return super(MediaSerializer, self).update(instance, validated_data)


class MediaDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    description = serializers.CharField()

    # 资源类型：10：电影 20：电视剧 30：综艺节目
    media_type = serializers.IntegerField()
    media_type_name = serializers.CharField(allow_null=True, allow_blank=True)
    # 题材类别  1：爱情 2：战争 3：校园 4：真人秀
    theme_type = serializers.IntegerField()
    theme_type_name = serializers.CharField(allow_null=True, allow_blank=True)
    # 项目进度  1：筹备期 2：策划期 3：xxx
    progress = serializers.IntegerField()
    progress_name = serializers.CharField(allow_null=True, allow_blank=True)

    # 模板类型 1：模板1  2：模板2
    template_type = serializers.IntegerField()
    # 标签：数据格式为JSON字符串，如：['综艺', '植入', '片头']
    tags = serializers.ListField()

    # 资源热度
    temperature = serializers.FloatField()
    # 票房预测
    box_office_forecast = serializers.FloatField()
    # 口碑预测
    public_praise_forecast = serializers.FloatField()
    # ROI 投资回报比 例如：1：5 （1比5）
    roi = serializers.CharField()

    # 资源概述 数据格式为字典形式的JSON字符串，如：{"导演": ["冯小刚", "吴宇森"],
    #                                        "主演": ["成龙", "李连杰"],
    #                                        "出演": ["巩俐", "章子怡"], ......}
    media_outline = serializers.DictField(allow_null=True)

    # 预计上映/播出时间
    air_time = serializers.DateTimeField()

    # 运营标记 0: 未设定 1：热门
    mark = serializers.IntegerField()

    # 电影表现大数据分析 数据格式为字典形式的JSON字符串，如：{"导演号召力": 3.5,
    #                                                "男主角号召力": 4.0,
    #                                                "女主角号召力": 4.2,
    #                                                "类型关注度": 3.8,
    #                                                "片方指数": 3.7}
    film_performance = serializers.DictField(allow_null=True)

    picture_profile = serializers.ImageField()
    picture_detail = serializers.ImageField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class MediaListSerializer(BaseListSerializer):
    child = MediaDetailSerializer()


class MediaConfigureSerializer(BaseModelSerializer):
    class Meta:
        model = MediaConfigure
        fields = '__all__'

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(MediaConfigureSerializer, self).update(instance, validated_data)


class MediaConfigureDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    media_id = serializers.IntegerField()
    media_name = serializers.CharField()
    dimension_id = serializers.IntegerField()
    dimension_name = serializers.CharField(allow_null=True, allow_blank=True)
    attribute_id = serializers.IntegerField()
    attribute_name = serializers.CharField(allow_null=True, allow_blank=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class MediaConfigureListSerializer(BaseListSerializer):
    child = MediaConfigureDetailSerializer()


class MediaTypeSerializer(BaseModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(MediaTypeSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(MediaTypeSerializer, self).update(instance, validated_data)


class MediaTypeListSerialzier(BaseListSerializer):
    child = MediaTypeSerializer()


class ThemeTypeSerializer(BaseModelSerializer):
    class Meta:
        model = ThemeType
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ThemeTypeSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(ThemeTypeSerializer, self).update(instance, validated_data)


class ThemeTypeDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    media_type_id = serializers.IntegerField()
    media_type_name = serializers.CharField()
    sort_order = serializers.IntegerField()
    status = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ThemeTypeListSerializer(BaseListSerializer):
    child = ThemeTypeDetailSerializer()


class ProjectProgressSerializer(BaseModelSerializer):
    class Meta:
        model = ProjectProgress
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ProjectProgressSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(ProjectProgressSerializer, self).update(instance, validated_data)


class ProjectProgressListSerializer(BaseListSerializer):
    child = ProjectProgressSerializer()


class ResourceTagSerializer(BaseModelSerializer):
    class Meta:
        model = ResourceTags
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ResourceTagSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(ResourceTagSerializer, self).update(instance, validated_data)


class ResourceTagListSerializer(BaseListSerializer):
    child = ResourceTagSerializer()


class ReportSerializer(BaseModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    def update(self, instance, validated_data):
        # 删除缓存
        BaseCache().delete_report_by_id(report_id=instance.id)

        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ReportSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        # 删除缓存
        BaseCache().delete_report_by_id(report_id=instance.id)

        validated_data = {'status': instance.id + 1}
        return super(ReportSerializer, self).update(instance, validated_data)


class ReportDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    description = serializers.CharField()

    media_id = serializers.IntegerField()
    media_name = serializers.CharField()
    # 标签：数据格式为JSON字符串，如：['行业月报', '综艺']
    tags = serializers.ListField()
    report_file = serializers.FileField()
    # 数据状态：1：正常  非1：已删除
    status = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ReportListSerializer(BaseListSerializer):
    child = ReportDetailSerializer()


class CommentSerializer(BaseModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update_recommend_status(self, instance, status=1):
        validated_data = {'is_recommend': status}
        return super(CommentSerializer, self).update(instance, validated_data)


class ReplyCommentSerializer(BaseModelSerializer):
    def __init__(self, instance=None, data=None, request=None, **kwargs):
        if data:
            data['user_id'] = request.user.id
            super(ReplyCommentSerializer, self).__init__(data=data, **kwargs)
        else:
            super(ReplyCommentSerializer, self).__init__(instance, **kwargs)

    class Meta:
        model = ReplyComment
        fields = '__all__'

    def save(self, **kwargs):
        # 删除缓存
        self.delete_data_from_cache(comment_id=self.initial_data['comment_id'])
        return super(ReplyCommentSerializer, self).save(**kwargs)

    def update(self, instance, validated_data):
        # 删除缓存
        self.delete_data_from_cache(comment_id=instance.comment_id)
        pop_keys = ['comment_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ReplyCommentSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        # 删除缓存
        self.delete_data_from_cache(comment_id=instance.comment_id)
        validated_data = {'status': instance.id + 1}
        return super(ReplyCommentSerializer, self).update(instance, validated_data)

    def delete_data_from_cache(self, comment_id):
        # 删除缓存
        BaseCache().delete_comment_detail_by_comment_id(comment_id)


class CommentAndReplyDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    source_type = serializers.IntegerField()
    source_id = serializers.IntegerField()
    content = serializers.CharField()
    is_recommend = serializers.IntegerField()
    like = serializers.IntegerField()
    dislike = serializers.IntegerField()
    reply_message = serializers.CharField(allow_null=True, allow_blank=True)
    source_title = serializers.CharField()
    created_for_user = serializers.DateTimeField()
    created_for_admin = serializers.DateTimeField(allow_null=True)


class CommentAndReplyListSerializer(BaseListSerializer):
    child = CommentAndReplyDetailSerializer()


class InformationSerializer(BaseModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

    def create_to_db(self, **kwargs):
        return super(InformationSerializer, self).create_to_db(**kwargs)

    def update(self, instance, validated_data):
        self.delete_data_from_cache(instance.pk)

        pop_keys = ['information_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(InformationSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        self.delete_data_from_cache(instance.pk)

        validated_data = {'status': instance.id + 1}
        return super(InformationSerializer, self).update(instance, validated_data)

    def delete_data_from_cache(self, information_id):
        # 删除缓存
        return BaseCache().delete_information_by_id(information_id)


class InformationDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    content = serializers.CharField()
    picture = serializers.ImageField()
    # 标签：数据格式为JSON字符串，如：['综艺', '植入', '片头']
    tags = serializers.ListField()
    # 浏览数
    read_count = serializers.IntegerField()
    # 点赞数量
    like = serializers.IntegerField()
    # 收藏数量
    collection_count = serializers.IntegerField()
    # 运营标记：0：无标记 1：重磅发布
    mark = serializers.IntegerField()
    # 栏目 0:无标记 1: 最新发布 2：电影大事件 3:娱乐营销观察 4:影片资讯
    column = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class InformationListSerializer(BaseListSerializer):
    child = InformationDetailSerializer()


class CaseSerializer(BaseModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

    def create_to_db(self, **kwargs):
        return super(CaseSerializer, self).create_to_db(**kwargs)

    def update(self, instance, validated_data):
        self.delete_data_from_cache(instance.pk)
        pop_keys = ['case_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(CaseSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        self.delete_data_from_cache(instance.pk)
        validated_data = {'status': instance.id + 1}
        return super(CaseSerializer, self).update(instance, validated_data)

    def delete_data_from_cache(self, case_id):
        # 删除缓存
        return BaseCache().delete_case_by_id(case_id)


class CaseDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    content = serializers.CharField()
    picture = serializers.ImageField()
    # 标签：数据格式为JSON字符串，如：['综艺', '植入', '片头']
    tags = serializers.ListField()
    # 浏览数
    read_count = serializers.IntegerField()
    # 点赞数量
    like = serializers.IntegerField()
    # 收藏数量
    collection_count = serializers.IntegerField()
    # 运营标记：0：无标记 1：重磅发布
    mark = serializers.IntegerField()
    # 栏目 0:无标记 1: 最新发布 2：电影大事件 3:娱乐营销观察 4:影片资讯
    column = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class CaseListSerializer(BaseListSerializer):
    child = CaseDetailSerializer()


class UserRoleSerializer(BaseModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def save(self, **kwargs):
        BaseCache().delete_user_role_list()
        return super(UserRoleSerializer, self).save(**kwargs)

    def update(self, instance, validated_data):
        BaseCache().delete_user_role_list()
        pop_keys = ['user_role_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(UserRoleSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        BaseCache().delete_user_role_list()
        validated_data = {'status': instance.id + 1}
        return super(UserRoleSerializer, self).update(instance, validated_data)


class UserRoleListSerializer(BaseListSerializer):
    child = UserRoleSerializer()


class AdjustCoefficientSerializer(BaseModelSerializer):
    class Meta:
        model = AdjustCoefficient
        fields = '__all__'

    def update(self, instance, validated_data):
        # 删除缓存
        BaseCache().delete_adjust_coefficient_by_name(adjust_coefficient_name=instance.name)
        pop_keys = ['pk', 'id', 'adjust_coefficient_id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(AdjustCoefficientSerializer, self).update(instance, validated_data)


class AdjustCoefficientListSerializer(BaseListSerializer):
    child = AdjustCoefficientSerializer()


class AdvertResourceSerializer(BaseModelSerializer):
    class Meta:
        model = AdvertResource
        fields = '__all__'

    def create_to_db(self, **kwargs):
        instance = super(AdvertResourceSerializer, self).create_to_db(**kwargs)
        if isinstance(instance, Exception):
            return instance

        self.delete_from_cache(instance)
        return instance

    def update(self, instance, validated_data):
        self.delete_from_cache(instance)

        pop_keys = ['pk', 'id', 'advert_resource_id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(AdvertResourceSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        self.delete_from_cache(instance)

        validated_data = {'status': instance.id + 1}
        return super(AdvertResourceSerializer, self).update(instance, validated_data)

    def delete_from_cache(self, instance):
        # 从缓存中删除数据
        BaseCache().delete_advert_list_by_source_type(instance.source_type)
        BaseCache().delete_advert_detail_by_advert_id(instance.id)


class AdvertResourceListSerializer(BaseListSerializer):
    child = AdvertResourceSerializer()

