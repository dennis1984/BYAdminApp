# -*- coding:utf8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.db import transaction
from decimal import Decimal

from horizon.models import (model_to_dict,
                            BaseManager,
                            get_perfect_filter_params)

import json
import datetime
import os


IMAGE_PICTURE_PATH = settings.PICTURE_DIRS['web']['tag']


class Dimension(models.Model):
    """
    维度
    """
    name = models.CharField('维度名称', max_length=32, db_index=True)
    subtitle = models.CharField('维度副标题', max_length=32, null=True, blank=True)
    description = models.CharField('维度描述', max_length=256, null=True, blank=True)

    sort_order = models.IntegerField('排序顺序', default=0)
    picture = models.ImageField('维度矢量图片', max_length=200,
                                upload_to=IMAGE_PICTURE_PATH,
                                default=os.path.join(IMAGE_PICTURE_PATH, 'noImage.png'))
    # 资源状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_dimension'
        unique_together = ('name', 'status')
        ordering = ['-updated']
        app_label = 'Web_App.web_dimensions.models.Dimension'

    class AdminMeta:
        fuzzy_fields = ['name']

    def __unicode__(self):
        return self.name

    @classmethod
    def get_object(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_objects(cls, fuzzy=True, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        if fuzzy:
            for key in kwargs.keys():
                if key in cls.AdminMeta.fuzzy_fields:
                    kwargs['%s__contains' % key] = kwargs.pop(key)
        try:
            instances = cls.objects.filter(**kwargs)
        except Exception as e:
            return e
        # 排序
        sort_instances = sorted(instances, key=lambda x: x.sort_order)
        key = -1
        for index, item in enumerate(sort_instances):
            if item.sort_order != 0:
                break
            key = index
        if key == -1:
            return sort_instances
        else:
            new_sort_list = sort_instances[key+1:]
            new_sort_list.extend(sort_instances[:key+1])
            return new_sort_list


class Attribute(models.Model):
    """
    属性
    """
    name = models.CharField('属性名称', max_length=64, db_index=True)
    description = models.CharField('描述', max_length=256, null=True, blank=True)
    dimension_id = models.IntegerField('所属维度ID')

    # picture = models.ImageField('属性矢量图片', max_length=200,
    #                             upload_to=IMAGE_PICTURE_PATH,
    #                             default=os.path.join(IMAGE_PICTURE_PATH, 'noImage.png'))
    # 资源状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_attribute'
        unique_together = ['name', 'status']
        ordering = ['dimension_id', '-updated']
        app_label = 'Web_App.web_dimensions.models.Attribute'

    class AdminMeta:
        fuzzy_fields = ['name']

    def __unicode__(self):
        return self.name

    @classmethod
    def get_object(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def get_detail(cls, **kwargs):
        instance = cls.get_object(**kwargs)
        if isinstance(instance, Exception):
            return instance

        dime_instance = Dimension.get_object(pk=instance.dimension_id)
        if isinstance(dime_instance, Exception):
            return dime_instance
        detail = model_to_dict(instance)
        detail['dimension_name'] = dime_instance.name
        return detail

    @classmethod
    def filter_objects(cls, fuzzy=True, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        if fuzzy:
            for key in kwargs.keys():
                if key in cls.AdminMeta.fuzzy_fields:
                    kwargs['%s__contains' % key] = kwargs.pop(key)
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_details(cls, **kwargs):
        instances = cls.filter_objects(**kwargs)
        if isinstance(instances, Exception):
            return instances

        details = []
        dime_dict = {}
        for ins in instances:
            dime_ins = dime_dict.get(ins.dimension_id)
            if not dime_ins:
                dime_ins = Dimension.get_object(pk=ins.dimension_id)
                if isinstance(dime_ins, Exception):
                    continue
                dime_dict[ins.dimension_id] = dime_ins

            item_detail = model_to_dict(ins)
            item_detail['dimension_name'] = dime_ins.name
            details.append(item_detail)
        return details


TAG_PICTURE_PATH = settings.PICTURE_DIRS['web']['tag']


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField('标签名称', max_length=64, db_index=True)
    description = models.CharField('描述', max_length=256, null=True, blank=True)

    picture = models.ImageField('简介图片', max_length=200,
                                upload_to=IMAGE_PICTURE_PATH,
                                default=os.path.join(IMAGE_PICTURE_PATH, 'noImage.png'))
    # picture_detail = models.ImageField('详情图片', max_length=200,
    #                                    upload_to=IMAGE_PICTURE_PATH,
    #                                    default=os.path.join(IMAGE_PICTURE_PATH, 'noImage.png'))

    # 数据状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_tag'
        unique_together = ['name', 'status']
        ordering = ['-updated']
        app_label = 'Web_App.web_dimensions.models.Tag'

    class AdminMeta:
        fuzzy_fields = ['name']
        origin_picture = 'picture'
        perfect_picture = {
            'max_disk_size': 1 * 1024 * 1024,
            'goal_picture': {
                'picture': {
                    'size': (75, 75),
                    'save_path': TAG_PICTURE_PATH,
                },
            },
        }

    def __unicode__(self):
        return self.name

    @classmethod
    def get_object(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_objects(cls, fuzzy=True, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        if fuzzy:
            for key in kwargs.keys():
                if key in cls.AdminMeta.fuzzy_fields:
                    kwargs['%s__contains' % key] = kwargs.pop(key)
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_objects_by_dimension_id(cls, dimension_id):
        attribute_instances = Attribute.filter_objects(dimension_id=dimension_id)
        attribute_ids = [ins.id for ins in attribute_instances]
        tag_config_instances = TagConfigure.filter_objects(attribute_id__in=attribute_ids)
        tag_ids = [ins.tag_id for ins in tag_config_instances]
        tag_instances = cls.filter_objects(id__in=list(set(tag_ids)))
        return tag_instances


class TagConfigure(models.Model):
    """
    标签配置
    """
    tag_id = models.IntegerField('标签ID', db_index=True)

    attribute_id = models.IntegerField('匹配属性ID')
    match_value = models.FloatField('与属性匹配值', default=1.0)

    # 数据状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_tag_configure'
        unique_together = ['tag_id', 'attribute_id', 'status']
        ordering = ['tag_id', 'attribute_id', '-updated']
        app_label = 'Web_App.web_dimensions.models.TagConfigure'

    def __unicode__(self):
        return '%s:%s' % (self.tag_id, self.attribute_id)

    @classmethod
    def get_object(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def get_detail(cls, **kwargs):
        instance = cls.get_object(**kwargs)
        if isinstance(instance, Exception):
            return instance

        tag_ins = Tag.get_object(pk=instance.tag_id)
        if isinstance(tag_ins, Exception):
            return tag_ins
        attr_ins = Attribute.get_object(pk=instance.attribute_id)
        if isinstance(attr_ins, Exception):
            return attr_ins

        detail = model_to_dict(instance)
        detail['tag_name'] = tag_ins.name
        detail['attribute_name'] = attr_ins.name
        return detail

    @classmethod
    def filter_objects(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_details(cls, **kwargs):
        instances = cls.filter_objects(**kwargs)
        if isinstance(instances, Exception):
            return instances

        tag_ins_dict = {}
        attr_ins_dict = {}
        details = []
        for ins in instances:
            tag_ins = tag_ins_dict.get(ins.tag_id)
            if not tag_ins:
                tag_ins = Tag.get_object(pk=ins.tag_id)
                if isinstance(tag_ins, Exception):
                    continue
            attr_ins = attr_ins_dict.get(ins.attribute_id)
            if not attr_ins:
                attr_ins = Attribute.get_object(pk=ins.attribute_id)
                if isinstance(attr_ins, Exception):
                    continue
            item_detail = model_to_dict(ins)
            item_detail['tag_name'] = tag_ins.name
            item_detail['attribute_name'] = attr_ins.name
            details.append(item_detail)
        return details


class AdjustCoefficient(models.Model):
    """
    调整系数
    """
    name = models.CharField('调整系数名称', max_length=64)
    description = models.CharField('字段描述', max_length=128)
    value = models.FloatField('调整值', default=0)

    # 数据状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_adjust_coefficient'
        app_label = 'Web_App.web_dimensions.models.AdjustCoefficient'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_object(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_objects(cls, **kwargs):
        kwargs = get_perfect_filter_params(cls, **kwargs)
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e
