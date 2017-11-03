# -*- coding:utf8 -*-
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.conf import settings

from horizon.models import model_to_dict
from horizon import main
from horizon.decorators import has_permission_to_update
from horizon.serializers import (BaseListSerializer,
                                 BaseModelSerializer,
                                 BaseSerializer,
                                 timezoneStringTostring)

from Web_App.web_dimensions.models import (Dimension,
                                           Attribute,
                                           TagConfigure, Tag)
from Web_App.web_media.models import (Media, MediaConfigure,
                                      MediaType, ThemeType,
                                      ProjectProgress,
                                      ResourceTags,
                                      Information, Case)
from Web_App.web_reports.models import Report, ReportDownloadRecord
from Web_App.web_comment.models import (Comment, ReplyComment)

import urllib
import os
import json
import re
import copy


class DimensionSerializer(BaseModelSerializer):
    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            super(DimensionSerializer, self).__init__(data=data, **kwargs)
        else:
            super(DimensionSerializer, self).__init__(instance, **kwargs)

    class Meta:
        model = Dimension
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['dimension_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(DimensionSerializer, self).update(instance, validated_data)

    def delete(self, instance):
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


class AttributeListSerializer(BaseListSerializer):
    child = AttributeSerializer()


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['tag_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(TagSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(TagSerializer, self).update(instance, validated_data)


class TagListSerializer(BaseListSerializer):
    child = TagSerializer()


class TagConfigureSerializer(BaseModelSerializer):
    class Meta:
        model = TagConfigure
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['tag_configure_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(TagConfigureSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(TagConfigureSerializer, self).update(instance, validated_data)


class TagConfigureListSerializer(BaseListSerializer):
    child = TagConfigureSerializer()


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
    dimension_name = serializers.CharField()
    attribute_id = serializers.IntegerField()
    attribute_name = serializers.CharField()
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
        pop_keys = ['pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ReportSerializer, self).update(instance, validated_data)

    def delete(self, instance):
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
    def __init__(self, request, instance=None, data=None, **kwargs):
        if data:
            data['user_id'] = request.user_id
            super(ReplyCommentSerializer, self).__init__(data=data, **kwargs)
        else:
            super(ReplyCommentSerializer, self).__init__(instance, **kwargs)

    class Meta:
        model = ReplyComment
        fields = '__all__'

    def update(self, instance, validated_data):
        pop_keys = ['comment_id', 'pk', 'id']
        for key in pop_keys:
            if key in validated_data:
                validated_data.pop(key)
        return super(ReplyCommentSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        validated_data = {'status': instance.id + 1}
        return super(ReplyCommentSerializer, self).update(instance, validated_data)


class CommentAndReplyDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    source_type = serializers.IntegerField()
    source_id = serializers.IntegerField()
    content = serializers.CharField()
    is_recommend = serializers.IntegerField()
    like = serializers.IntegerField()
    dislike = serializers.IntegerField()
    reply_message = serializers.CharField()
    source_title = serializers.CharField()


class CommentAndReplyListSerializer(BaseListSerializer):
    child = CommentAndReplyDetailSerializer()

