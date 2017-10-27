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
                               UserInstanceSerializer,
                               UserDetailSerializer,
                               UserListSerializer,
                               IdentifyingCodeSerializer,)
from users.permissions import IsOwnerOrReadOnly
from users.models import (User,
                          make_token_expire,
                          IdentifyingCode,)
from users.forms import (CreateUserForm,
                         SendIdentifyingCodeForm,
                         SendIdentifyingCodeWithLoginForm,
                         VerifyIdentifyingCodeForm,
                         UpdateUserInfoForm,
                         SetPasswordForm,
                         PhoneForm,
                         EmailForm)

from horizon.views import APIView
from horizon.main import make_random_number_of_string
from horizon import main
import copy
import urllib


def verify_identifying_code(params_dict):
    """
    验证验证码
    """
    username = params_dict['username']
    identifying_code = params_dict['identifying_code']

    instance = IdentifyingCode.get_object_by_phone_or_email(username)
    if not instance:
        return Exception(('Identifying code is not existed or expired.',))
    if instance.identifying_code != identifying_code:
        return Exception(('Identifying code is incorrect.',))
    return True


class IdentifyingCodeAction(APIView):
    """
    send identifying code to a phone
    """
    def verify_phone(self, cld):
        instance = User.get_object_by_username(username_type=cld['username_type'],
                                               username=cld['username'])
        if cld['method'] == 'register':     # 用户注册
            if isinstance(instance, User):
                return Exception('The phone or email is already registered.')
        elif cld['method'] == 'forget_password':   # 忘记密码
            if isinstance(instance, Exception):
                return Exception('The user of the phone or email is not existed.')
        else:
            return Exception('Parameters Error.')
        return True

    def is_request_data_valid(self, **kwargs):
        if kwargs['username_type'] == 'phone':
            form = PhoneForm({'phone': kwargs['username']})
            if not form.is_valid():
                return False, form.errors
        elif kwargs['username_type'] == 'email':
            form = EmailForm({'email': kwargs['username']})
            if not form.is_valid():
                return False, form.errors
        return True, None

    def send_identifying_code(self, identifying_code, **kwargs):
        # 发送到短信平台
        if kwargs['username_type'] == 'phone':
            main.send_message_to_phone({'code': identifying_code},
                                       (kwargs['username'],))
        elif kwargs['username_type'] == 'email':
            # 发送邮件
            _to = [kwargs['username']]
            subject = '验证码'
            text = '您的验证码是%s, 15分钟有效。' % identifying_code
            main.send_email(_to, subject, text)

    def post(self, request, *args, **kwargs):
        """
        发送验证码
        """
        form = SendIdentifyingCodeForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        result = self.verify_phone(cld)
        if isinstance(result, Exception):
            return Response({'Detail': result.args}, status=status.HTTP_400_BAD_REQUEST)

        identifying_code = make_random_number_of_string(str_length=6)
        serializer = IdentifyingCodeSerializer(data={'phone_or_email': cld['username'],
                                                     'identifying_code': identifying_code})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # 发送验证码
        self.send_identifying_code(identifying_code, **cld)
        return Response(status=status.HTTP_200_OK)


class IdentifyingCodeActionWithLogin(generics.GenericAPIView):
    """
    发送短信验证码（登录状态）
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def send_identifying_code(self, identifying_code, **kwargs):
        # 发送到短信平台
        if kwargs['username_type'] == 'phone':
            main.send_message_to_phone({'code': identifying_code},
                                       (kwargs['username'],))
        elif kwargs['username_type'] == 'email':
            # 发送邮件
            _to = [kwargs['username']]
            subject = '验证码'
            text = '您的验证码是%s, 15分钟有效。' % identifying_code
            main.send_email(_to, subject, text)

    def is_request_data_valid(self, request, **kwargs):
        if 'username' in kwargs:
            if kwargs['username_type'] == 'phone':
                if request.user.is_binding(kwargs['username_type']):
                    if kwargs['username'] != request.user.phone:
                        return False, 'The phone number is incorrect.'
                else:
                    user = User.get_object_by_username(**kwargs)
                    if isinstance(user, User):
                        return False, 'The phone number is already binding.'
            elif kwargs['username_type'] == 'email':
                if request.user.is_binding(kwargs['username_type']):
                    if kwargs['username'] != request.user.email:
                        return False, 'The email is incorrect.'
                else:
                    user = User.get_object_by_username(**kwargs)
                    if isinstance(user, User):
                        return False, 'The email is already binding.'
        else:
            if not request.user.is_binding(kwargs['username_type']):
                return False, 'Your phone or email is not existed.'
        return True, None

    def post(self, request, *args, **kwargs):
        form = SendIdentifyingCodeWithLoginForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(request, **cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        if 'username' not in cld:
            if cld['username_type'] == 'phone':
                cld['username'] = request.user.phone
            else:
                cld['username'] = request.user.email
        identifying_code = make_random_number_of_string(str_length=6)
        serializer = IdentifyingCodeSerializer(data={'phone_or_email': cld['username'],
                                                     'identifying_code': identifying_code})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        self.send_identifying_code(identifying_code, **cld)
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
        result = verify_identifying_code(cld)
        if isinstance(result, Exception):
            return Response({'Detail': result.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Result': result}, status=status.HTTP_200_OK)


class UserNotLoggedAction(APIView):
    """
    create user API
    """
    def get_object_by_username(self, phone):
        return User.get_object(**{'phone': phone})

    def is_request_data_valid(self, **kwargs):
        if kwargs['username_type'] == 'phone':
            form = PhoneForm({'phone': kwargs['username']})
            if not form.is_valid():
                return False, form.errors
        elif kwargs['username_type'] == 'email':
            form = EmailForm({'email': kwargs['username']})
            if not form.is_valid():
                return False, form.errors
        return True, None

    def post(self, request, *args, **kwargs):
        """
        用户注册
        """
        form = CreateUserForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        result = verify_identifying_code(cld)
        if isinstance(result, Exception):
            return Response({'Detail': result.args}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(**cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserInstanceSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        忘记密码
        """
        form = SetPasswordForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        result = verify_identifying_code(cld)
        if isinstance(result, Exception):
            return Response({'Detail': result.args}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object_by_username(cld['phone'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance)
        try:
            serializer.update_password(request, instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        # serializer_response = UserInstanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class UserAction(generics.GenericAPIView):
    """
    update user API
    """
    permission_classes = (IsOwnerOrReadOnly, )

    def get_object_of_user(self, request):
        return User.get_object(**{'pk': request.user.id})

    def get_perfect_validate_data(self, **cleaned_data):
        return cleaned_data

    def put(self, request, *args, **kwargs):
        """
        更新用户信息
        """
        form = UpdateUserInfoForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        cld = self.get_perfect_validate_data(**cld)
        serializer = UserSerializer(request.user)
        try:
            serializer.update_userinfo(request, request.user, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class UserDetail(generics.GenericAPIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def get_user_object(self, request):
        return User.get_user_detail(request)

    def post(self, request, *args, **kwargs):
        user_detail = self.get_user_object(request)
        if isinstance(user_detail, Exception):
            return Response({'Detail': user_detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserDetailSerializer(data=user_detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
