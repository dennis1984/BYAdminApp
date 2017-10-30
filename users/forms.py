# -*- encoding: utf-8 -*-
from horizon import forms


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=20, min_length=11,
                            error_messages={
                                'required': u'手机号不能为空',
                                'min_length': u'手机号位数不够'
                            })


class PasswordForm(forms.Form):
    password = forms.CharField(min_length=6,
                               max_length=50,
                               error_messages={
                                   'required': u'密码不能为空',
                                   'min_length': u'密码长度不能少于6位'
                               })
    # confirm_password = forms.CharField(min_length=6,
    #                                    max_length=50,
    #                                    error_messages={
    #                                        'required': u'密码不能为空',
    #                                        'min_length': u'密码长度不能少于6位'
    #                                    })


class SendIdentifyingCodeForm(forms.Form):
    """
    发送手机/邮箱验证码（未登录状态）
    """
    username = forms.CharField(max_length=200)


class SendIdentifyingCodeWithLoginForm(forms.Form):
    """
    发送手机/邮箱验证码（登录状态）
    """
    username = forms.CharField(max_length=200)


class VerifyIdentifyingCodeForm(PhoneForm):
    """
    验证手机验证码
    """
    identifying_code = forms.CharField(max_length=10,
                                       error_messages={'required': u'验证码不能为空'})


class UpdateUserInfoForm(forms.Form):
    """
    更改用户信息
    """
    nickname = forms.CharField(max_length=100, required=False)
    head_picture = forms.ImageField(required=False)


class UpdatePasswordForm(forms.Form):
    """
    更新密码
    """
    password = forms.CharField(min_length=6, max_length=50)
    identifying_code = forms.CharField(min_length=6, max_length=10,
                                       error_messages={
                                           'required': u'验证码不能为空'
                                       })


class CreateUserForm(PasswordForm):
    """
    用户注册
    """
    username = forms.CharField(max_length=200)
    identifying_code = forms.CharField(min_length=6, max_length=10,
                                       error_messages={
                                           'required': u'验证码不能为空'
                                       })


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=200)


class SetPasswordForm(PasswordForm):
    """
    忘记密码
    """
    username = forms.CharField(max_length=200)
    identifying_code = forms.CharField(min_length=6, max_length=10,
                                       error_messages={
                                           'required': u'验证码不能为空'
                                       })


class UserListForm(forms.Form):
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)

