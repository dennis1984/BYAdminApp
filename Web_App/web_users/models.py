# -*- coding:utf8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.conf import settings
from oauth2_provider.models import AccessToken
from horizon.models import (model_to_dict,
                            get_perfect_filter_params,
                            BaseManager)
import datetime
import re
import os


class Role(models.Model):
    """
    用户角色
    """
    name = models.CharField('角色名称', max_length=32, db_index=True, unique=True)
    # 数据状态：1：正常  非1：已删除
    status = models.IntegerField('数据状态', default=1)
    created = models.DateTimeField('创建时间', default=now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    objects = BaseManager()

    class Meta:
        db_table = 'by_user_role'
        app_label = 'Web_App.web_users.models.Role'

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
            if cls.AdminMeta.fuzzy_fields:
                for key in kwargs:
                    if key in cls.AdminMeta.fuzzy_fields:
                        kwargs['%s__contains' % key] = kwargs.pop(key)
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e
