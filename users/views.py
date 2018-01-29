# -*- coding: utf8 -*-
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.views.mixins import OAuthLibMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from users.serializers import (UserSerializer,
                               UserListSerializer,
                               IdentifyingCodeSerializer,
                               UserDetailSerializer)
from users.permissions import IsOwnerOrReadOnly
from users.models import (User,
                          make_token_expire,
                          IdentifyingCode,)
from users.forms import (CreateUserForm,
                         SendIdentifyingCodeForm,
                         SendIdentifyingCodeWithLoginForm,
                         VerifyIdentifyingCodeForm,
                         UpdateUserInfoForm,
                         UpdatePasswordForm,
                         SetPasswordForm,
                         UserListForm)

from horizon.views import APIView
from horizon.main import make_random_number_of_string
from horizon import main
import copy
import urllib


def verify_identifying_code(**kwargs):
    """
    验证验证码
    """
    username = kwargs['username']
    identifying_code = kwargs['identifying_code']

    instance = IdentifyingCode.get_object_by_username(username)
    if not instance:
        return False, 'Identifying code is not existed or expired.'
    if instance.identifying_code != identifying_code:
        return False, 'Identifying code is incorrect.',
    return True, None


class IdentifyingCodeAction(APIView):
    """
    send identifying code to a phone
    """
    def verify_phone(self, cld):
        instance = User.get_object_by_username(username=cld['username'])
        # 忘记密码
        if isinstance(instance, Exception):
            return False, 'The user of the phone or email is not existed.'
        return True, None

    def send_identifying_code(self, identifying_code, username):
        # 发送到短信平台
        main.send_phone_message_for_5_platform(identifying_code, username)

    def post(self, request, *args, **kwargs):
        """
        发送验证码
        """
        form = SendIdentifyingCodeForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.verify_phone(cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        identifying_code = make_random_number_of_string(str_length=6)
        serializer = IdentifyingCodeSerializer(data={'phone': cld['username'],
                                                     'identifying_code': identifying_code})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # 发送验证码
        self.send_identifying_code(identifying_code, cld['username'])
        return Response(status=status.HTTP_200_OK)


class IdentifyingCodeActionWithLogin(generics.GenericAPIView):
    """
    发送短信验证码（登录状态）
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def send_identifying_code(self, identifying_code, username):
        # 发送到短信平台
        main.send_phone_message_for_5_platform(identifying_code, username)

    def post(self, request, *args, **kwargs):
        form = SendIdentifyingCodeWithLoginForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        identifying_code = make_random_number_of_string(str_length=6)
        serializer = IdentifyingCodeSerializer(data={'phone': cld['username'],
                                                     'identifying_code': identifying_code})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

        self.send_identifying_code(identifying_code, cld['username'])
        return Response(status=status.HTTP_200_OK)


class IdentifyingCodeVerify(APIView):
    def post(self, request, *args, **kwargs):
        """
        验证手机验证码
        """
        form = VerifyIdentifyingCodeForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        cld = form.cleaned_data
        is_valid, error_message = verify_identifying_code(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Result': is_valid}, status=status.HTTP_200_OK)


class UserNotLoggedAction(APIView):
    """
    create user API
    """
    def get_object_by_username(self, phone):
        return User.get_object(**{'phone': phone})

    # def is_request_data_valid(self, **kwargs):
    #     if kwargs['username_type'] == 'phone':
    #         form = PhoneForm({'phone': kwargs['username']})
    #         if not form.is_valid():
    #             return False, form.errors
    #     elif kwargs['username_type'] == 'email':
    #         form = EmailForm({'email': kwargs['username']})
    #         if not form.is_valid():
    #             return False, form.errors
    #     return True, None

    # def post(self, request, *args, **kwargs):
    #     """
    #     用户注册
    #     """
    #     form = CreateUserForm(request.data)
    #     if not form.is_valid():
    #         return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     cld = form.cleaned_data
    #     is_valid, error_message = self.is_request_data_valid(**cld)
    #     if not is_valid:
    #         return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
    #     result = verify_identifying_code(**cld)
    #     if isinstance(result, Exception):
    #         return Response({'Detail': result.args}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         user = User.objects.create_user(**cld)
    #     except Exception as e:
    #         return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = UserInstanceSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        忘记密码
        """
        form = SetPasswordForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = verify_identifying_code(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object_by_username(cld['username'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance)
        try:
            serializer.update_password(request, instance, cld['password'])
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class UserAction(generics.GenericAPIView):
    """
    update user API
    """
    permission_classes = (IsOwnerOrReadOnly, )

    def does_username_exist(self, username):
        user = User.get_object(phone=username)
        if isinstance(user, Exception):
            return False
        return True

    def get_perfect_request_data(self, **kwargs):
        kwargs['phone'] = kwargs.pop('username')
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        创建管理员用户
        """
        form = CreateUserForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        does_username_exist = self.does_username_exist(cld['username'])
        if does_username_exist:
            return Response({'Detail': 'The phone number does exist.'})

        cld = self.get_perfect_request_data(**cld)
        serializer = UserSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = UserDetailSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新用户信息
        """
        form = UpdateUserInfoForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = UserSerializer(request.user)
        try:
            serializer.update_userinfo(request, request.user, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def patch(self, request, *args, **kwargs):
        """
        更新密码 
        """
        form = UpdatePasswordForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        verify_params = {'username': request.user.phone,
                         'identifying_code': cld['identifying_code']}
        is_valid, error_message = verify_identifying_code(**verify_params)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(request.user)
        try:
            serializer.update_password(request, request.user, cld['password'])
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Detail': serializer.data}, status=status.HTTP_206_PARTIAL_CONTENT)


class UserDetail(generics.GenericAPIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def get_user_object(self, request):
        return User.get_object(id=request.user.id)

    def post(self, request, *args, **kwargs):
        user = self.get_user_object(request)
        if isinstance(user, Exception):
            return Response({'Detail': user.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(generics.GenericAPIView):
    """
    用户列表
    """
    permission_classes = (IsOwnerOrReadOnly, )

    def get_user_list(self, **kwargs):
        return User.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = UserListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        user_list = self.get_user_list()
        serializer = UserListSerializer(user_list)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class AuthLogin(OAuthLibMixin, View):
    """
    用户认证：登录
    """
    def post(self, request, *args, **kwargs):
        return redirect(reverse('oauth2_provider.token'))


class AuthLogout(generics.GenericAPIView):
    """
    用户认证：登出
    """
    def post(self, request, *args, **kwargs):
        make_token_expire(request)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
