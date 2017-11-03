# -*- encoding: utf-8 -*-
from horizon import forms


class DimensionActionForm(forms.Form):
    name = forms.CharField(max_length=32)
    subtitle = forms.CharField(max_length=32)
    description = forms.CharField(max_length=256)
    sort_order = forms.IntegerField(min_value=1)
    picture = forms.ImageField()


class DimensionUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=32, required=False)
    subtitle = forms.CharField(max_length=32, required=False)
    description = forms.CharField(max_length=256, required=False)
    sort_order = forms.IntegerField(min_value=1, required=False)
    picture = forms.ImageField(required=False)


class DimensionDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class DimensionDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class DimensionListForm(forms.Form):
    name = forms.CharField(max_length=32, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class AttributeInputForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256, required=False)
    dimension_id = forms.IntegerField(min_value=1)
    picture = forms.ImageField(required=False)


class AttributeUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=256, required=False)
    picture = forms.ImageField(required=False)


class AttributeDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class AttributeDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class AttributeListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    dimension_id = forms.IntegerField(min_value=1, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class TagInputForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256, required=False)
    picture_profile = forms.ImageField()
    picture_detail = forms.ImageField()


class TagUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=256, required=False)
    picture_profile = forms.ImageField(required=False)
    picture_detail = forms.ImageField(required=False)


class TagDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class TagDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class TagListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class TagConfigureInputForm(forms.Form):
    tag_id = forms.IntegerField(min_value=1)
    attribute_id = forms.IntegerField(min_value=1)
    match_value = forms.FloatField(min_value=0.1, max_value=5.0)


class TagConfigureUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    # attribute_id = forms.IntegerField(min_value=1, required=False)
    match_value = forms.FloatField(min_value=0.1, max_value=5.0, required=False)


class TagConfigureDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class TagConfigureDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class TagConfigureListForm(forms.Form):
    tag_name = forms.CharField(max_length=64, required=False)
    tag_id = forms.IntegerField(min_value=1, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class MediaInputForm(forms.Form):
    title = forms.CharField(max_length=128)
    subtitle = forms.CharField(max_length=128)
    description = forms.CharField()

    template_type = forms.ChoiceField(choices=((1, 1),
                                               (2, 2)),
                                      error_messages={
                                          'required': 'Template type must in [1, 2]'
                                      })

    # 标签：数据格式为JSON字符串，如：['综艺', '植入', '片头']
    tags = forms.CharField()

    temperature = forms.FloatField(min_value=0.1, max_value=10.0)
    box_office_forecast = forms.FloatField(min_value=0.1, max_value=5.0)
    public_praise_forecast = forms.FloatField(min_value=0.1, max_value=5.0)

    # 导演：数据格式为JSON字符串，如：['斯皮尔伯格', '冯小刚']
    director = forms.CharField(max_length=256)
    # 主演：数据格式为JSON字符串，如：['汤姆克鲁斯', '威尔史密斯', '皮尔斯布鲁斯南']
    stars = forms.CharField(max_length=256)
    # 演员：数据格式为JSON字符串，如：['王晓霞', '詹姆斯', '韦德']
    actors = forms.CharField(max_length=256)
    # 监制：数据格式为JSON字符串，如：['欧文']
    producer = forms.CharField(max_length=256)
    # 出品公司：数据格式为JSON字符串，如：['华文映像', '福星传媒']
    production_company = forms.CharField(max_length=256)

    # 预计开机/录制时间
    recorded_time = forms.DateTimeField()
    # 预计上映/播出时间
    air_time = forms.DateTimeField()
    # 预计播出平台：数据格式为JSON字符串，如：['一线卫视', '视频网络渠道']
    play_platform = forms.CharField(max_length=256)

    # 运营标记 0: 未设定 1：热门
    mark = forms.ChoiceField(choices=((0, 1),
                                      (1, 2)),
                             error_messages={
                                 'required': 'mark must in [0, 1]'
                             })

    picture_profile = forms.ImageField()
    picture_detail = forms.ImageField()
    picture_hd = forms.ImageField()


class MediaConfigureInputForm(forms.Form):
    media_id = forms.IntegerField(min_value=1)
    dimension_id = forms.IntegerField(min_value=1)
    attribute_id = forms.IntegerField(min_value=1)


class MediaConfigureDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class MediaConfigureDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class MediaConfigureListForm(forms.Form):
    media_name = forms.CharField(max_length=128, required=False)
    dimension_name = forms.CharField(max_length=32, required=False)
    attribute_name = forms.CharField(max_length=64, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class MediaTypeInputForm(forms.Form):
    name = forms.CharField(max_length=64)


class MediaTypeUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)


class MediaTypeDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class MediaTypeDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class MediaTypeListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class ThemeTypeInputForm(forms.Form):
    name = forms.CharField(max_length=64)
    media_type_id = forms.IntegerField(min_value=1)


class ThemeTypeUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)
    media_type_id = forms.IntegerField(min_value=1, required=False)


class ThemeTypeDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ThemeTypeDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ThemeTypeListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    media_type_id = forms.IntegerField(min_value=1, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class ProjectProgressInputForm(forms.Form):
    name = forms.CharField(max_length=64)


class ProjectProgressUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)


class ProjectProgressDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ProjectProgressDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ProjectProgressListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class ResourceTagInputForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256, required=False)


class ResourceTagUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    name = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=256, required=False)


class ResourceTagDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ResourceTagDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ResourceTagListForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class ReportInputForm(forms.Form):
    title = forms.CharField(max_length=32)
    subtitle = forms.CharField(max_length=128)
    description = forms.CharField()
    media_id = forms.IntegerField(min_value=1)
    # 标签：数据格式为JSON字符串，如：['行业月报', '综艺']
    tags = forms.CharField(max_length=256)
    # 报告文件
    report_file = forms.FileField()


class ReportUpdateForm(forms.Form):
    id = forms.IntegerField(min_value=1)
    title = forms.CharField(max_length=32, required=False)
    subtitle = forms.CharField(max_length=128, required=False)
    description = forms.CharField(required=False)
    media_id = forms.IntegerField(min_value=1, required=False)
    # 标签：数据格式为JSON字符串，如：['行业月报', '综艺']
    tags = forms.CharField(max_length=256, required=False)
    # 报告文件
    report_file = forms.FileField(required=False)


class ReportDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ReportDetailForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class ReportListForm(forms.Form):
    title = forms.CharField(max_length=32, required=False)
    media_name = forms.CharField(max_length=32, required=False)
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)


class ReplyCommentInputForm(forms.Form):
    comment_id = forms.IntegerField(min_value=1)
    message = forms.CharField()


class ReplyCommentUpdateForm(forms.Form):
    comment_id = forms.IntegerField(min_value=1)
    message = forms.CharField()


class ReplyCommentDeleteForm(forms.Form):
    comment_id = forms.IntegerField(min_value=1)


class CommentAndReplyDetailForm(forms.Form):
    comment_id = forms.IntegerField(min_value=1)


class CommentAndReplyListForm(forms.Form):
    page_size = forms.IntegerField(min_value=1, required=False)
    page_index = forms.IntegerField(min_value=1, required=False)
