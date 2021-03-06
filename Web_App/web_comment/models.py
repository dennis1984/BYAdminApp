# -*- coding:utf8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now

from Web_App.web_media.models import Media, Information, Case
from horizon.models import (model_to_dict,
                            get_perfect_filter_params,
                            BaseManager)

import json
import datetime


SOURCE_TYPE_DB = {1: Media,   # 资源
                  2: Case,   # 案例
                  3: Information,   # 资讯
                  }


class Comment(models.Model):
    """
    用户点评
    """
    user_id = models.IntegerField('用户ID', db_index=True)

    # 点评资源类型： 1：资源 2：案例 3：资讯
    source_type = models.IntegerField('点评资源类型', default=1)
    # 资源数据ID
    source_id = models.IntegerField('点评资源ID')
    content = models.CharField('点评内容', max_length=512)

    # 是否被管理员推荐该评论: 0: 否  1：是
    is_recommend = models.IntegerField('是否被管理员推荐', default=0)
    like = models.IntegerField('喜欢数量', default=0)
    dislike = models.IntegerField('不喜欢数量', default=0)

    # 数据状态：1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_comment'
        unique_together = ['user_id', 'source_type', 'source_id']
        index_together = ['source_type', 'source_id']
        ordering = ['-created']
        app_label = 'Web_App.web_comment.models.Comment'

    def __unicode__(self):
        return '%s:%s:%s' % (self.user_id, self.source_type, self.source_id)

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
        return instance.perfect_detail

    @property
    def perfect_detail(self):
        is_recommend = self.is_recommend
        reply_message = ''
        created_for_admin = None
        if is_recommend:
            reply = ReplyComment.get_object(comment_id=self.pk)
            reply_message = reply.message
            created_for_admin = reply.updated
        source_ins = self.get_source_object(source_type=self.source_type,
                                            source_id=self.source_id)
        if isinstance(source_ins, Exception):
            source_title = ''
        else:
            source_title = source_ins.title
        item_dict = model_to_dict(self)
        item_dict['is_recommend'] = is_recommend
        item_dict['reply_message'] = reply_message
        item_dict['source_title'] = source_title
        item_dict['created_for_user'] = item_dict['created']
        item_dict['created_for_admin'] = created_for_admin
        return item_dict

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
        details = []
        for ins in instances:
            details.append(ins.perfect_detail)
        return details

    @classmethod
    def get_source_object(cls, source_type, source_id):
        source_class = SOURCE_TYPE_DB.get(source_type)
        if not source_class:
            return Exception('Params is incorrect')

        return source_class.get_object(pk=source_id)


class ReplyComment(models.Model):
    """
    管理员回复点评
    """
    comment_id = models.IntegerField(u'被回复点评的记录ID', db_index=True)
    user_id = models.IntegerField('管理员用户ID')
    message = models.TextField('点评回复', null=True, blank=True)

    # 数据状态 1：正常 非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_reply_comment'
        unique_together = ['comment_id', 'status']
        app_label = 'Web_App.web_comment.models.ReplyComment'

    def __unicode__(self):
        return str(self.comment_id)

    @classmethod
    def get_object(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e
