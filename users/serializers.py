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
from users.models import User, IdentifyingCode

import urllib
import os
import json
import re
import copy


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'nickname', 'head_picture',)

    @has_permission_to_update
    def update_password(self, request, instance, password):
        validated_data = {'password': make_password(password)}
        return super(UserSerializer, self).update(instance, validated_data)

    @has_permission_to_update
    def update_userinfo(self, request, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    def binding_phone_or_email_to_user(self, request, instance, validated_data):
        if validated_data['username_type'] == 'phone':
            _validated_data = {'phone': validated_data['username']}
        else:
            _validated_data = {'email': validated_data['username']}
        return super(UserSerializer, self).update(instance, _validated_data)

    def save(self, **kwargs):
        data = self.validated_data
        phone = data.pop('phone')
        password = data.pop('password')
        return User.objects.create_superuser(username=phone, password=password, **kwargs)


class UserDetailSerializer(BaseSerializer):
    id = serializers.IntegerField()
    phone = serializers.CharField(allow_blank=True, allow_null=True)
    # email = serializers.EmailField(allow_blank=True, allow_null=True)
    nickname = serializers.CharField(allow_blank=True, allow_null=True)

    last_login = serializers.DateTimeField()
    head_picture = serializers.ImageField()


class UserListSerializer(BaseListSerializer):
    child = UserSerializer()


class IdentifyingCodeSerializer(BaseModelSerializer):
    class Meta:
        model = IdentifyingCode
        fields = '__all__'
