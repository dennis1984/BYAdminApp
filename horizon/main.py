# -*- coding:utf8 -*-
from oauthlib.common import generate_token
from django.conf import settings
from django.utils.timezone import now
from lxml import etree
import datetime
import qrcode
import json
import os
import uuid
from hashlib import md5
from barcode import generate
from barcode.writer import ImageWriter
import base64
import random
import time
import copy

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate


def minutes_5_plus():
    return now() + datetime.timedelta(minutes=5)


def minutes_15_plus():
    return now() + datetime.timedelta(minutes=15)


def minutes_30_plus():
    return now() + datetime.timedelta(minutes=30)


def days_7_plus():
    return now() + datetime.timedelta(days=7)


def make_time_delta(days=0, hours=0, minutes=0, seconds=0):
    """
    设置时间增量
    """
    return now() + datetime.timedelta(days=days,
                                      hours=hours,
                                      minutes=minutes,
                                      seconds=seconds)


def make_time_delta_for_custom(date_time, days=0, hours=0, minutes=0, seconds=0):
    """
    设置时间增量
    """
    return date_time + datetime.timedelta(days=days,
                                          hours=hours,
                                          minutes=minutes,
                                          seconds=seconds)


def make_perfect_time_delta(days=0, hours=0, minutes=0, seconds=0):
    """
    设置时间增量
    """
    now_date = datetime.datetime.strftime(now().date(), '%Y-%m-%d %H:%M:%S')
    now_datetime = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M:%S')
    return now_datetime + datetime.timedelta(days=days,
                                             hours=hours,
                                             minutes=minutes,
                                             seconds=seconds)


class DatetimeEncode(json.JSONEncoder):
    """
    让json模块可以序列化datetime类型的字段
    """
    def default(self, o):
        from django.db.models.fields.files import ImageFieldFile

        if isinstance(o, datetime.datetime):
            return str(o)
        elif isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)


def timezoneStringTostring(timezone_string):
    """
    rest framework用JSONRender方法格式化datetime.datetime格式的数据时，
    生成数据样式为：2017-05-19T09:40:37.227692Z 或 2017-05-19T09:40:37Z
    此方法将数据样式改为："2017-05-19 09:40:37"，
    返回类型：string
    """
    if not isinstance(timezone_string, (str, unicode)):
        return ""
    if not timezone_string:
        return ""
    timezone_string = timezone_string.split('.')[0]
    timezone_string = timezone_string.split('Z')[0]
    try:
        timezone = datetime.datetime.strptime(timezone_string, '%Y-%m-%dT%H:%M:%S')
    except:
        return ""
    return str(timezone)


QRCODE_PICTURE_PATH = settings.PICTURE_DIRS['admin']['qrcode']


def make_qrcode(source_data, save_path=QRCODE_PICTURE_PATH, version=5):
    """
    生成二维码图片
    """
    qr = qrcode.QRCode(version=version,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(source_data)
    qr.make(fit=True)
    fname = "%s.png" % make_random_char_and_number_of_string(20)
    fname_path = os.path.join(save_path, fname)

    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    image = qr.make_image()
    image.save(fname_path)
    return fname_path


def make_barcode(save_path=QRCODE_PICTURE_PATH, barcode_length=8):
    """
    生成条形码
    返回：条形码数字及条形码文件名
    """
    source_data = make_random_number_of_string(barcode_length)
    generate_dict = {8: {'name': 'EAN8',
                         'width': 0.96},
                     13: {'name': 'EAN13',
                          'width': 0.66}
                     }
    fname = '%s.png' % make_random_char_and_number_of_string(20)
    fname_path = os.path.join(save_path, fname)
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    fp = open(fname_path, 'wb')
    writer = ImageWriter()
    generate_name = generate_dict[barcode_length]['name']
    width = generate_dict[barcode_length]['width']
    generate(generate_name, source_data, writer=writer, output=fp,
             writer_options={'module_width': width,
                             'module_height': 30})
    fp.close()

    return writer.text, fname_path


def make_static_url_by_file_path(file_path):
    path_list = file_path.split('static/', 1)
    return os.path.join(settings.WEB_URL_FIX, 'static', path_list[1])


def anaysize_xml_to_dict(source):
    """
    解析xml字符串
    """
    root = etree.fromstring(source)
    result = {article.tag: article.text for article in root}
    return result


def make_dict_to_xml(source_dict, use_cdata=True):
    """
    生成xml字符串
    """
    if not isinstance(source_dict, dict):
        raise ValueError('Parameter must be dict.')

    xml = etree.Element('xml')
    for _key, _value in source_dict.items():
        _key_xml = etree.SubElement(xml, _key)
        if _key == 'detail':
            _key_xml.text = etree.CDATA(_value)
        else:
            if not isinstance(_value, (bytes, unicode)):
                _value = unicode(_value)
            if use_cdata:
                _key_xml.text = etree.CDATA(_value)
            else:
                _key_xml.text = _value

    xml_string = etree.tostring(xml,
                                pretty_print=True,
                                encoding="UTF-8",
                                method="xml",
                                xml_declaration=True,
                                standalone=None)
    return xml_string.split('\n', 1)[1]


def make_sign_for_wxpay(source_dict):
    """
    生成签名（微信支付）
    """
    key_list = []
    for _key in source_dict:
        if not source_dict[_key] or _key == 'sign':
            continue
        key_list.append({'key': _key, 'value': source_dict[_key]})
    key_list.sort(key=lambda x: x['key'])

    string_param = ''
    for item in key_list:
        string_param += '%s=%s&' % (item['key'], item['value'])
        # 把密钥和其它参数组合起来
    # string_param += 'key=%s' % wx_settings.KEY
    md5_string = md5(string_param.encode('utf8')).hexdigest()
    return md5_string.upper()


# def verify_sign_for_alipay(params_str, source_sign):
#     """
#     支付宝支付验证签名（公钥验证签名）
#     """
#     pub_key = RSA.importKey(open(ali_settings.ALI_PUBLIC_KEY_FILE_PATH))
#     source_sign = base64.b64decode(source_sign)
#     _sign = SHA256.new(params_str)
#     verifer = PKCS1_v1_5.new(pub_key)
#     return verifer.verify(_sign, source_sign)


def make_dict_to_verify_string(params_dict):
    """
    将参数字典转换成待签名的字符串
    """
    params_list = []
    for key, value in params_dict.items():
        if not value or key == 'sign':
            continue
        params_list.append({'key': key, 'value': value})
    params_list.sort(key=lambda x: x['key'])
    params_strs = []
    for item in params_list:
        params_strs.append('%s=%s' % (item['key'], (item['value']).encode('utf8')))
    return '&'.join(params_strs)


def make_random_number_of_string(str_length=6):
    """
    生成数字型的随机字符串（最大长度：128位）
    """
    if str_length > 128:
        str_length = 128
    random_str = _random_str = str(random.random()).split('.')[1]
    for i in range(str_length / len(_random_str)):
        random_str += str(random.random()).split('.')[1]
    index_start = random.randint(0, len(random_str) - str_length)
    return random_str[index_start: index_start + str_length]


def make_random_char_and_number_of_string(str_length=32):
    """
    生成英文字符和数字混合型的字符串（最大长度：128位）
    """
    if str_length > 128:
        str_length = 128
    return generate_token(length=str_length)


def get_time_stamp():
    stamp = str(time.time()).split('.')[0]
    return stamp


def send_message_to_phone(params, receive_phones, template_name=None):
    """
    使用阿里云的短信服务发送短信
    """
    from horizon.http_requests import send_http_request
    import urllib
    url = 'http://sms.market.alicloudapi.com/singleSendSms'
    AppCode = '2e8a1a8a3e22486b9be6ac46c3d2c6ec'
    sign_names = ('吟食',)
    template_dict = {'register': 'SMS_91765097',
                     'recharge': 'SMS_102170028'}
    params_key_dict = {'register': 'code',
                       'recharge': 'count'}

    if not template_name:
        template = template_dict['register']
    else:
        if template_name not in template_dict.keys():
            return ValueError('Params template incorrect')
        template = template_dict[template_name]
    if isinstance(params, (str, unicode, int, float)):
        if isinstance(params, (float, int)):
            params_dict = {params_key_dict[template_name]: '%.2f' % params}
        else:
            params_dict = {params_key_dict[template_name]: params}
        params_query = urllib.quote(json.dumps(params_dict))
    elif isinstance(params, dict):
        params_query = urllib.quote(json.dumps(params))
    else:
        return TypeError('params must be unicode or dictionary')

    if isinstance(receive_phones, (str, unicode)):
        receive_phones = [receive_phones]
    else:
        if not isinstance(receive_phones, (tuple, list)):
            return TypeError('receive phones type must be list or tuple')
    query = {'RecNum': ','.join(receive_phones),
             'TemplateCode': template,
             'SignName': sign_names[0]}
    query_str = '%s&ParamString=%s' % (urllib.urlencode(query), params_query)

    return send_http_request(url, query_str, add_header={'Authorization': 'APPCODE %s' % AppCode})


def send_email(to, subject, text, files=()):
    """
    发送邮件
    使用影联客的邮箱用户名和密码
    """
    assert isinstance(to, (list, tuple))

    server = {'host': 'smtp.163.com',
              'port': 465,
              'user': 'year2005706',
              'password': 'xxx',
              'prefix': '影联客',
              'postfix': '163.com'}

    _from = '%s@%s' % (server['user'], server['postfix'])

    message = MIMEMultipart()
    message['From'] = '%s<%s>' % (server['prefix'], _from)
    message['Subject'] = subject
    message['To'] = COMMASPACE.join(to)
    message['Date'] = formatdate(localtime=True)
    message.attach(MIMEText(text, _subtype='plain', _charset='utf8'))

    try:
        smtp = smtplib.SMTP_SSL(server['host'], server['port'])
        smtp.login(server['user'], server['password'])
        smtp.sendmail(_from, to, message.as_string())
        smtp.close()
    except:
        return False

    return True


def select_random_element_from_array(source_list, count):
    """
    从列表中随机取出一定数量的元素
    """
    if not isinstance(source_list, (list, tuple)):
        return ValueError('Params "source_list" type incorrect')
    if len(source_list) <= count:
        return source_list

    range_list = [i for i in range(len(source_list))]
    random_index_list = []
    for i in range(count):
        pop_index = random.choice(range_list)
        random_index_list.append(pop_index)
        range_list.remove(pop_index)
    new_list = [source_list[index] for index in random_index_list]
    return new_list


# 图片处理类
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.core.files.uploadedfile import InMemoryUploadedFile
import cStringIO

MEDIA_IMAGE_PATH = settings.PICTURE_DIRS['web']['media']


class BaseImage(object):
    """
    图片处理类：提供缩略图、等比例压缩图和裁决图片
    """
    save_path = MEDIA_IMAGE_PATH
    quality = 85
    image_format = 'JPEG'
    max_disk_size = 1 * 1024 * 1024  # 最大占用磁盘空间大小
    max_size = (None, None)     # 最大分辨率
    min_size = (320, 200)       # 最小分辨率
    postfix_format_dict = {'JPEG': 'jpg',
                           'PNG': 'png'}

    def __init__(self, image_name=None, image=None, image_size=0, **kwargs):
        if image:
            self.image = image
        else:
            try:
                self.image = Image.open(image_name)
            except Exception as e:
                raise Exception(e)

        if not image_size:
            self.image_size = self.get_image_size(self.image)
        else:
            self.image_size = image_size
        for key in kwargs:
            if key in ('max_size', 'min_size'):
                if not isinstance(kwargs[key], (tuple, list)):
                    raise TypeError('Params [max_size, min_size] must be tuple or list.')
            setattr(self, key, kwargs[key])

        # 判断图片分辨率是否太小
        if self.is_too_small:
            raise TypeError('The image size is too small.')

        self.close_alpha()
        # 判断图片是否大于限定的最大值
        if self.image_size > self.max_disk_size:
            ratio = self.max_disk_size / float(self.image_size)
            self.image = self.resize(ratio)

    @classmethod
    def get_image_size(cls, image):
        buff = cStringIO.StringIO(image.fp.read())
        disk_size = len(buff.read())
        buff.close()
        return disk_size

    @classmethod
    def to_in_memory_uploaded_file(cls, image, field_name, name):
        disk_size = cls.get_image_size(image)
        return InMemoryUploadedFile(file=image,
                                    field_name=field_name,
                                    name=name,
                                    content_type='image/%s' % cls.postfix_format_dict[image.format],
                                    size=disk_size,
                                    charset='utf8')

    @property
    def is_too_small(self):
        if self.image.size < self.min_size:
            return True

    @property
    def is_too_big(self):
        if self.max_size:
            if self.image.size > self.max_size:
                return True

    def compress(self, width=0, height=0, image_format=None):
        """
        缩略图
        返回：新图片对象
        """
        # if not save_path:
        #     save_path = self.save_path
        # if not image_format:
        #     image_format = self.image_format
        # file_name = '%s.%s' % (make_random_char_and_number_of_string(12),
        #                        self.postfix_format_dict[image_format])
        # file_path = os.path.join(save_path, file_name)
        new_image = copy.copy(self.image)
        try:
            new_image.thumbnail(width, height)
            # new_image.save(file_path, image_format.upper())
        except Exception as e:
            return e
        return new_image

    def resize(self, ratio, quality=None, image_format=None):
        """
        等比例缩放
        返回：新图片对象
        """
        if ratio >= 1:
            return TypeError('Params [ratio] is incorrect.')

        # if not quality:
        #     quality = self.quality
        # if not save_path:
        #     save_path = self.save_path
        # if not image_format:
        #     image_format = self.image_format
        new_image = copy.copy(self.image)
        origin_width, origin_height = self.image.size

        # file_name = '%s.%s' % (make_random_char_and_number_of_string(12),
        #                        self.postfix_format_dict[image_format])
        # file_path = os.path.join(save_path, file_name)
        new_image.resize((int(origin_width*ratio), int(origin_height*ratio)), Image.ANTIALIAS)
        # new_image.save(file_path, image_format.upper(), quality=quality)
        return new_image

    def clip_resize(self, goal_width=0, goal_height=0, image_format=None, quality=None):
        """
        裁决及等比例缩放 
        返回：新图片对象
        """
        # if not image_format:
        #     image_format = self.image_format
        # if not quality:
        #     quality = self.quality
        # file_name = '%s.%s' % (make_random_char_and_number_of_string(12),
        #                        self.postfix_format_dict[image_format])
        # file_path = os.path.join(save_path, file_name)

        origin_width, origin_height = self.image.size
        if goal_width > origin_width or goal_height > origin_height:
            return ValueError('Params [goal_width] or [goal_height] is incorrect.')

        goal_ratio = goal_height / float(goal_width)
        origin_ratio = origin_height / float(origin_width)
        if origin_ratio >= goal_ratio:   # 原图过高
            height = origin_width * goal_ratio
            width = origin_width
            x = 0
            y = (origin_height - height) / 2
        else:  # 原图过宽
            height = origin_height
            width = origin_height / goal_ratio
            y = 0
            x = (origin_width - width) / 2

        new_image = copy.copy(self.image)
        box = (x, y, width + x, height + y)
        # 剪切图片
        new_image = new_image.crop(box)

        # 压缩图片
        try:
            new_image.resize((int(goal_width), int(goal_height), Image.ANTIALIAS))
            # new_image.save(file_path, image_format.upper(), quality=quality)
        except Exception as e:
            return e
        return new_image

    def close_alpha(self):
        """
        如果图片格式是PNG，并且alpha通道是开启的，
        则将图片转化为JPEG格式，以此节省磁盘空间。
        """
        if self.image.mode == 'RGBA':
            # 使用白色来填充背景
            new_image = Image.new('RGBA', self.image.size, (255, 255, 255))
            new_image.paste(self.image,
                            (0, 0, self.image.size[0], self.image.size[1]),
                            self.image)

            # 关闭Alpha通道
            # new_file_name = '%s.jpg' % os.path.join(
            #     os.path.dirname(self.image.filename),
            #     os.path.basename(self.image.filename).split('.', 1)[0]
            # )
            # new_image.save(new_file_name, 'JPEG')
            tmp_image = Image.new('RGB', self.image.size, (255, 255, 255))
            tmp_image.paste(new_image,
                            (0, 0, self.image.size[0], self.image.size[1]),
                            new_image)
            self.image = tmp_image



