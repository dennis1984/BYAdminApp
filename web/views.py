# -*- coding: utf8 -*-
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from web.serializers import (DimensionSerializer,
                             DimensionListSerializer,
                             AttributeSerializer,
                             AttributeDetailSerializer,
                             AttributeListSerializer,
                             TagSerializer,
                             TagListSerializer,
                             TagConfigureSerializer,
                             TagConfigureDetailSerializer,
                             TagConfigureListSerializer,
                             MediaConfigureSerializer,
                             MediaConfigureDetailSerializer,
                             MediaConfigureListSerializer,
                             MediaTypeSerializer,
                             MediaTypeListSerialzier,
                             ThemeTypeSerializer,
                             ThemeTypeDetailSerializer,
                             ThemeTypeListSerializer,
                             ProjectProgressSerializer,
                             ProjectProgressListSerializer,
                             ResourceTagSerializer,
                             ResourceTagListSerializer,
                             ReportSerializer,
                             ReportDetailSerializer,
                             ReportListSerializer,
                             ReplyCommentSerializer,
                             CommentAndReplyDetailSerializer,
                             CommentAndReplyListSerializer,
                             CommentSerializer,
                             InformationSerializer,
                             InformationDetailSerializer,
                             InformationListSerializer,
                             CaseSerializer,
                             CaseDetailSerializer,
                             CaseListSerializer,
                             MediaSerializer,
                             MediaDetailSerializer,
                             MediaListSerializer)
from web.permissions import IsOwnerOrReadOnly
from web.forms import (DimensionActionForm,
                       DimensionUpdateForm,
                       DimensionDeleteForm,
                       DimensionDetailForm,
                       DimensionListForm,
                       AttributeInputForm,
                       AttributeUpdateForm,
                       AttributeDeleteForm,
                       AttributeDetailForm,
                       AttributeListForm,
                       TagInputForm,
                       TagUpdateForm,
                       TagDeleteForm,
                       TagDetailForm,
                       TagListForm,
                       TagConfigureInputForm,
                       TagConfigureUpdateForm,
                       TagConfigureDeleteForm,
                       TagConfigureDetailForm,
                       TagConfigureListForm,
                       MediaConfigureInputForm,
                       MediaConfigureDeleteForm,
                       MediaConfigureDetailForm,
                       MediaConfigureListForm,
                       MediaTypeInputForm,
                       MediaTypeUpdateForm,
                       MediaTypeDeleteForm,
                       MediaTypeDetailForm,
                       MediaTypeListForm,
                       ThemeTypeInputForm,
                       ThemeTypeUpdateForm,
                       ThemeTypeDeleteForm,
                       ThemeTypeDetailForm,
                       ThemeTypeListForm,
                       ProjectProgressInputForm,
                       ProjectProgressUpdateForm,
                       ProjectProgressDetailForm,
                       ProjectProgressDeleteForm,
                       ProjectProgressListForm,
                       ResourceTagInputForm,
                       ResourceTagUpdateForm,
                       ResourceTagDeleteForm,
                       ResourceTagDetailForm,
                       ResourceTagListForm,
                       ReportInputForm,
                       ReportUpdateForm,
                       ReportDeleteForm,
                       ReportDetailForm,
                       ReportListForm,
                       ReplyCommentInputForm,
                       ReplyCommentUpdateForm,
                       ReplyCommentDeleteForm,
                       CommentAndReplyDetailForm,
                       CommentAndReplyListForm,
                       InformationInputForm,
                       InformationUpdateForm,
                       InformationDeleteForm,
                       InformationDetailForm,
                       InformationListForm,
                       CaseInputForm,
                       CaseUpdateForm,
                       CaseDeleteForm,
                       CaseDetailForm,
                       CaseListForm,
                       MediaInputForm,
                       MediaUpdateForm,
                       MediaDeleteForm,
                       MediaDetailForm,
                       MediaListForm)
from Web_App.web_dimensions.models import (Dimension,
                                           Attribute,
                                           Tag,
                                           TagConfigure)
from Web_App.web_media.models import (Media,
                                      MediaConfigure,
                                      MediaType, ThemeType,
                                      ProjectProgress,
                                      ResourceTags,
                                      Information, Case)
from Web_App.web_reports.models import Report, ReportDownloadRecord
from Web_App.web_comment.models import (Comment, ReplyComment)

from horizon.views import APIView
from horizon.main import make_random_number_of_string
from horizon import main
import copy
import urllib
import json


class DimensionAction(generics.GenericAPIView):
    """
    维度操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_dimension_object(self, dimension_id):
        return Dimension.get_object(pk=dimension_id)

    def post(self, request, *args, **kwargs):
        """
        添加维度信息
        """
        form = DimensionActionForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = DimensionSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新维度信息
        """
        form = DimensionUpdateForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_dimension_object(dimension_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DimensionSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        删除维度信息
        """
        form = DimensionDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_dimension_object(dimension_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DimensionSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class DimensionDetail(generics.GenericAPIView):
    """
    维度详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_dimension_object(self, dimension_id):
        return Dimension.get_object(pk=dimension_id)

    def post(self, request, *args, **kwargs):
        form = DimensionDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_dimension_object(dimension_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DimensionSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DimensionList(generics.GenericAPIView):
    """
    维度详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_dimension_list(self, **kwargs):
        return Dimension.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = DimensionListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instances = self.get_dimension_list(**cld)
        serializer = DimensionListSerializer(instances)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(list_data, status=status.HTTP_200_OK)


class AttributeAction(generics.GenericAPIView):
    """
    属性操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_attribute_object(self, attribute_id):
        return Attribute.get_object(pk=attribute_id)

    def is_request_data_valid(self, **kwargs):
        if 'dimension_id' in kwargs:
            dime_ins = Dimension.get_object(pk=kwargs['dimension_id'])
            if isinstance(dime_ins, Exception):
                return False, dime_ins.args
        return True, None

    def post(self, request, *args, **kwargs):
        """
        添加属性信息
        """
        form = AttributeInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新信息
        """
        form = AttributeUpdateForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_attribute_object(attribute_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        删除信息
        """
        form = AttributeDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_attribute_object(attribute_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class AttributeDetail(generics.GenericAPIView):
    """
    属性详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_attribute_detail(self, attribute_id):
        return Attribute.get_detail(pk=attribute_id)

    def post(self, request, *args, **kwargs):
        form = AttributeDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_attribute_detail(attribute_id=cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttributeList(generics.GenericAPIView):
    """
    属性详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_attribute_list(self, **kwargs):
        if 'dimension_name' in kwargs:
            dime_instances = Dimension.filter_objects(name=kwargs['dimension_name'])
            if isinstance(dime_instances, Exception):
                return dime_instances
            kwargs['dimension_id__in'] = [ins.id for ins in dime_instances]
            kwargs.pop('dimension_name')
        return Attribute.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = AttributeListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_attribute_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttributeListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(list_data, status=status.HTTP_200_OK)


class TagAction(generics.GenericAPIView):
    """
    标签操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_object(self, tag_id):
        return Tag.get_object(pk=tag_id)

    def post(self, request, *args, **kwargs):
        """
        添加标签信息
        """
        form = TagInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = TagSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.create_to_db()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新信息
        """
        form = TagUpdateForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_tag_object(tag_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        删除信息
        """
        form = TagDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_tag_object(tag_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TagDetail(generics.GenericAPIView):
    """
    标签详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_object(self, tag_id):
        return Tag.get_object(pk=tag_id)

    def post(self, request, *args, **kwargs):
        form = TagDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_tag_object(tag_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagList(generics.GenericAPIView):
    """
    标签详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_list(self, **kwargs):
        return Tag.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = TagListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instances = self.get_tag_list(**cld)
        serializer = TagListSerializer(instances)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(list_data, status=status.HTTP_200_OK)


class TagConfigureAction(generics.GenericAPIView):
    """
    标签配置操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_object(self, tag_id):
        return Tag.get_object(pk=tag_id)

    def get_attribute_object(self, attribute_id):
        return Attribute.get_object(pk=attribute_id)

    def get_tag_configure_object(self, tag_configure_id):
        return TagConfigure.get_object(pk=tag_configure_id)

    def is_request_data_valid(self, **kwargs):
        tag_instance = self.get_tag_object(tag_id=kwargs['tag_id'])
        if isinstance(tag_instance, Exception):
            return False, tag_instance.args

        attribute_instance = self.get_attribute_object(attribute_id=kwargs['attribute_id'])
        if isinstance(attribute_instance, Exception):
            return False, attribute_instance.args

        return True, None

    def post(self, request, *args, **kwargs):
        """
        添加标签配置信息
        """
        form = TagConfigureInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagConfigureSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新信息
        """
        form = TagConfigureUpdateForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_tag_configure_object(tag_configure_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        # attr_instance = self.get_attribute_object(attribute_id=cld['attribute_id'])
        # if isinstance(attr_instance, Exception):
        #     return Response({'Detail': attr_instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TagConfigureSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        删除信息
        """
        form = TagConfigureDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_tag_configure_object(tag_configure_id=cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagConfigureSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TagConfigureDetail(generics.GenericAPIView):
    """
    标签配置详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_configure_detail(self, tag_configure_id):
        return TagConfigure.get_detail(pk=tag_configure_id)

    def post(self, request, *args, **kwargs):
        form = TagConfigureDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_tag_configure_detail(tag_configure_id=cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagConfigureDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagConfigureList(generics.GenericAPIView):
    """
    标签配置详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_tag_object(self, **kwargs):
        return Tag.get_object(**kwargs)

    def get_tag_configure_list(self, **kwargs):
        if 'tag_name' in kwargs:
            tag_instances = Tag.filter_objects(name=kwargs['tag_name'])
            if isinstance(tag_instances, Exception):
                return tag_instances
            # if 'tag_id' in kwargs:
            #     if kwargs['tag_id'] != tag_instance.id:
            #         return Exception('The instance does not exist.')
            # else:
            #     kwargs['tag_id'] = tag_instance.id
            kwargs['tag_id__in'] = [ins.id for ins in tag_instances]
            kwargs.pop('tag_name')
        if 'attribute_name' in kwargs:
            attr_instances = Attribute.filter_objects(name=kwargs['attribute_name'])
            if isinstance(attr_instances, Exception):
                return attr_instances
            kwargs['attribute_id__in'] = [ins.id for ins in attr_instances]
            kwargs.pop('attribute_name')

        return TagConfigure.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = TagConfigureListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_tag_configure_list(**cld)
        serializer = TagConfigureListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(list_data, status=status.HTTP_200_OK)


class MediaTypeAction(generics.GenericAPIView):
    """
    资源类型操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_type_object(self, media_type_id):
        return MediaType.get_object(pk=media_type_id)

    def post(self, request, *args, **kwargs):
        form = MediaTypeInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = MediaTypeSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = MediaTypeUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_media_type_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaTypeSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = MediaTypeDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_media_type_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaTypeSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaTypeDetail(generics.GenericAPIView):
    """
    资源类型详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_type_object(self, media_type_id):
        return MediaType.get_object(pk=media_type_id)

    def post(self, request, *args, **kwargs):
        form = MediaTypeDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_media_type_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaTypeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaTypeList(generics.GenericAPIView):
    """
    资源类型详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_type_list(self, **kwargs):
        return MediaType.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = MediaTypeListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instances = self.get_media_type_list(**cld)
        if isinstance(instances, Exception):
            return Response({'Detail': instances.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaTypeListSerialzier(instances)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)

        return Response(list_data, status=status.HTTP_200_OK)


class ThemeTypeAction(generics.GenericAPIView):
    """
    题材类型操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def is_request_data_valid(self, **kwargs):
        media_type_ins = MediaType.get_object(pk=kwargs['media_type_id'])
        if isinstance(media_type_ins, Exception):
            return False, media_type_ins.args
        return True, None

    def get_theme_type_object(self, theme_type_id):
        return ThemeType.get_object(pk=theme_type_id)

    def post(self, request, *args, **kwargs):
        form = ThemeTypeInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemeTypeSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = ThemeTypeUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_theme_type_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemeTypeSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self,request, *args, **kwargs):
        form = ThemeTypeDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_theme_type_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemeTypeSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ThemeTypeDetail(generics.GenericAPIView):
    """
    题材类型详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_theme_type_detail(self, theme_type_id):
        return ThemeType.get_detail(pk=theme_type_id)

    def post(self, request, *args, **kwargs):
        form = ThemeTypeDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_theme_type_detail(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemeTypeDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ThemeTypeList(generics.GenericAPIView):
    """
    题材类型详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_theme_type_detail_list(self, **kwargs):
        if 'media_type_name' in kwargs:
            media_type_instances = MediaType.filter_objects(name=kwargs['media_type_name'])
            if isinstance(media_type_instances, Exception):
                return media_type_instances
            kwargs['media_type_id__in'] = [ins.id for ins in media_type_instances]
            kwargs.pop('media_type_name')
        return ThemeType.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = ThemeTypeListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_theme_type_detail_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemeTypeListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class ProjectProgressAction(generics.GenericAPIView):
    """
    项目进度操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_project_progress_object(self, project_progress_id):
        return ProjectProgress.get_object(pk=project_progress_id)

    def post(self, request, *args, **kwargs):
        form = ProjectProgressInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = ProjectProgressSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = ProjectProgressUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_project_progress_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectProgressSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = ProjectProgressDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_project_progress_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectProgressSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectProgressDetail(generics.GenericAPIView):
    """
    项目进度详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_project_progress_object(self, project_progress_id):
        return ProjectProgress.get_object(pk=project_progress_id)

    def post(self, request, *args, **kwargs):
        form = ProjectProgressDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_project_progress_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectProgressSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectProgressList(generics.GenericAPIView):
    """
    项目进度详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_project_progress_list(self, **kwargs):
        return ProjectProgress.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = ProjectProgressListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instances = self.get_project_progress_list(**cld)
        if isinstance(instances, Exception):
            return Response({'Detail': instances.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectProgressListSerializer(instances)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class MediaAction(generics.GenericAPIView):
    """
    媒体资源操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_object(self, media_id):
        return Media.get_object(pk=media_id)

    def get_media_type_object(self, media_type_id):
        return MediaType.get_object(pk=media_type_id)

    def get_theme_type_object(self, theme_type_id):
        return ThemeType.get_object(pk=theme_type_id)

    def is_request_data_valid(self, **kwargs):
        if 'tags' in kwargs:
            try:
                tags = json.loads(kwargs['tags'])
            except Exception as e:
                return False, e.args
            if not isinstance(tags, (list, tuple)):
                return False, 'Params [tags] is incorrect.'
            for item in tags:
                if not isinstance(item, int):
                    return False, 'Params [tags] is incorrect.'
                tag_ins = ResourceTags.get_object(pk=item)
                if isinstance(tag_ins, Exception):
                    return False, tag_ins.args
        if 'theme_type_id' in kwargs:
            theme_type_ins = ThemeType.get_object(pk=kwargs['theme_type_id'])
            if isinstance(theme_type_ins, Exception):
                return False, theme_type_ins.args
        if 'progress_id' in kwargs:
            progress_ins = ProjectProgress.get_object(pk=kwargs['progress_id'])
            if isinstance(progress_ins, Exception):
                return False, progress_ins.args
        if 'media_outline' in kwargs:
            try:
                media_outline = json.loads(kwargs['media_outline'])
            except Exception as e:
                return False, e.args
            if not isinstance(media_outline, dict):
                return False, 'Params [media_outline] is incorrect.'
            for key, item_value in media_outline.items():
                if not isinstance(key, (str, unicode)) or \
                        not isinstance(item_value, (str, unicode)):
                    return False, 'Params [media_outline] is incorrect.'
        return True, None

    def post(self, request, *args, **kwargs):
        """
        新建媒体资源
        """
        form = MediaInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        theme_type_ins = self.get_theme_type_object(cld['theme_type_id'])
        media_type_ins = self.get_media_type_object(theme_type_ins.media_type_id)
        if isinstance(media_type_ins, Exception):
            return Response({'Detail': media_type_ins.args}, status=status.HTTP_400_BAD_REQUEST)

        cld['media_type_id'] = media_type_ins.id
        serializer = MediaSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.create_to_db()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        更新媒体资源信息
        """
        form = MediaUpdateForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_media_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MediaSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        删除媒体资源信息
        """
        form = MediaDeleteForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_media_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MediaSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaDetail(generics.GenericAPIView):
    """
    媒体资源详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_detail(self, media_id):
        return Media.get_detail(pk=media_id)

    def post(self, request, *args, **kwargs):
        form = MediaDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_media_detail(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaList(generics.GenericAPIView):
    """
    媒体资源详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_list(self, **kwargs):
        return Media.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = MediaListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_media_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class MediaConfigureAction(generics.GenericAPIView):
    """
    媒体资源配置操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_dimension_object(self, dimension_id):
        return Dimension.get_object(pk=dimension_id)

    def get_attribute_object(self, attribute_id):
        return Attribute.get_object(pk=attribute_id)

    def get_perfect_request_data(self, **kwargs):
        attr_instance = self.get_attribute_object(kwargs['attribute_id'])
        dime_instance = self.get_dimension_object(attr_instance.dimension_id)
        if isinstance(dime_instance, Exception):
            return dime_instance
        kwargs['dimension_id'] = dime_instance.pk
        return kwargs

    def is_request_data_valid(self, **kwargs):
        media_instance = Media.get_object(pk=kwargs['media_id'])
        if isinstance(media_instance, Exception):
            return False, media_instance.args
        attr_instance = self.get_attribute_object(kwargs['attribute_id'])
        if isinstance(attr_instance, Exception):
            return False, attr_instance.args
        return True, None

    def get_media_configure_object(self, media_configure_id):
        return MediaConfigure.get_object(pk=media_configure_id)

    def post(self, request, *args, **kwargs):
        form = MediaConfigureInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        cld = self.get_perfect_request_data(**cld)
        if isinstance(cld, Exception):
            return Response({'Detail': cld.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaConfigureSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def put(self, request, *args, **kwargs):
    #     pass

    def delete(self, request, *args, **kwargs):
        form = MediaConfigureDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_media_configure_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaConfigureSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Detail': serializer.data}, status=status.HTTP_204_NO_CONTENT)


class MediaConfigureDetail(generics.GenericAPIView):
    """
    媒体资源配置详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_configure_detail(self, media_configure_id):
        return MediaConfigure.get_detail(pk=media_configure_id)

    def post(self, request, *args, **kwargs):
        form = MediaConfigureDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_media_configure_detail(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaConfigureDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaConfigureList(generics.GenericAPIView):
    """
    媒体资源配置详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_media_configure_list(self, **kwargs):
        pop_keys = ['media_name', 'dimension_name', 'attribute_name']
        model_select_dict = {'media_name': {'model': Media,
                                            'selector': {'title': kwargs.get('media_name')}},
                             'dimension_name': {'model': Dimension,
                                                'selector': {'name': kwargs.get('dimension_name')}},
                             'attribute_name': {'model': Attribute,
                                                'selector': {'name': kwargs.get('attribute_name')}}
                             }
        for p_key in pop_keys:
            if p_key in kwargs:
                model = model_select_dict[p_key]['model']
                _kw = model_select_dict[p_key]['selector']
                instances = model.filter_objects(**_kw)
                if isinstance(instances, Exception):
                    return instances
                kwargs['%s_id__in' % p_key.split('_')[0]] = [ins.id for ins in instances]
                kwargs.pop(p_key)

        return MediaConfigure.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = MediaConfigureListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_media_configure_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MediaConfigureListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class ResourceTagAction(generics.GenericAPIView):
    """
    资源标签操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_resource_tag_object(self, resource_tag_id):
        return ResourceTags.get_object(pk=resource_tag_id)

    def post(self, request, *args, **kwargs):
        form = ResourceTagInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        serializer = ResourceTagSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = ResourceTagUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_resource_tag_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResourceTagSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = ResourceTagDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_resource_tag_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResourceTagSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceTagDetail(generics.GenericAPIView):
    """
    资源标签详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_resource_tag_object(self, resource_tag_id):
        return ResourceTags.get_object(pk=resource_tag_id)

    def post(self, request, *args, **kwargs):
        form = ResourceTagDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_resource_tag_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ResourceTagSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResourceTagList(generics.GenericAPIView):
    """
    资源标签详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_resource_tag_list(self, **kwargs):
        return ResourceTags.filter_objects(**kwargs)

    def post(self, request, *args, **kwargs):
        form = ResourceTagListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instances = self.get_resource_tag_list(**cld)
        if isinstance(instances, Exception):
            return Response({'Detail': instances.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResourceTagListSerializer(instances)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class ReportAction(generics.GenericAPIView):
    """
    报告文件操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_report_object(self, report_id):
        return Report.get_object(pk=report_id)

    def is_request_data_valid(self, **kwargs):
        if 'media_id' in kwargs:
            media_ins = Media.get_object(pk=kwargs['media_id'])
            if isinstance(media_ins, Exception):
                return False, media_ins.args
        if 'tags' in kwargs:
            try:
                tags = json.loads(kwargs['tags'])
            except Exception as e:
                return False, e.args
            else:
                if not isinstance(tags, (list, tuple)):
                    return False, 'Tags type error.'
        return True, None

    def post(self, request, *args, **kwargs):
        form = ReportInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        form = ReportUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_report_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = ReportDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_report_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportDetail(generics.GenericAPIView):
    """
    报告文件详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_report_object(self, report_id):
        return Report.get_detail(pk=report_id)

    def post(self, request, *args, **kwargs):
        form = ReportDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_report_object(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportList(generics.GenericAPIView):
    """
    报告文件详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_report_list(self, **kwargs):
        return Report.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = ReportListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_report_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class ReplyCommentAction(generics.GenericAPIView):
    """
    管理员回复评论操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_comment_object(self, comment_id):
        return Comment.get_object(pk=comment_id)

    def get_reply_comment_object(self, comment_id):
        return ReplyComment.get_object(comment_id=comment_id)

    def is_request_data_valid(self, method=None, **kwargs):
        comment_ins = Comment.get_object(pk=kwargs['comment_id'])
        if isinstance(comment_ins, Exception):
            return False, None, None, comment_ins.args

        reply_ins = ReplyComment.get_object(comment_id=kwargs['comment_id'])
        if method == 'create':
            if isinstance(reply_ins, ReplyComment):
                return False, None, None, 'Can not repeat reply comment.'
        elif method in ['update', 'delete']:
            if isinstance(reply_ins, Exception):
                return False, None, None, reply_ins.args

        return True, comment_ins, reply_ins, None

    def post(self, request, *args, **kwargs):
        form = ReplyCommentInputForm(request.data, request.FILES)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        (is_valid, comment_ins,
         reply_ins, error_message) = self.is_request_data_valid(method='create', **cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReplyCommentSerializer(data=cld, request=request)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        comment_serializer = CommentSerializer(comment_ins)
        try:
            serializer.save()
            comment_serializer.update_recommend_status(comment_ins, status=1)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        form = ReplyCommentUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        (is_valid, comment_ins,
         reply_ins, error_message) = self.is_request_data_valid(method='update', **cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        # if isinstance(reply_ins, Exception):
        #     return Response({'Detail': reply_ins.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReplyCommentSerializer(reply_ins)
        try:
            serializer.update(reply_ins, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = ReplyCommentDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        (is_valid, comment_ins,
         reply_ins, error_message) = self.is_request_data_valid(method='delete', **cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(reply_ins, Exception):
            return Response({'Detail': reply_ins.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReplyCommentSerializer(reply_ins)
        comment_serializer = CommentSerializer(comment_ins)
        try:
            serializer.delete(reply_ins)
            comment_serializer.update_recommend_status(comment_ins, status=0)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAndReplyDetail(generics.GenericAPIView):
    """
    用户评论和管理员回复详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_comment_and_reply_detailt(self, comment_id):
        return Comment.get_detail(pk=comment_id)

    def post(self, request, *args, **kwargs):
        form = CommentAndReplyDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_comment_and_reply_detailt(cld['comment_id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentAndReplyDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentAndReplyList(generics.GenericAPIView):
    """
    用户评论和管理员回复详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_comment_and_reply_list(self, **kwargs):
        return Comment.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = CommentAndReplyListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_comment_and_reply_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentAndReplyListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class InformationAction(generics.GenericAPIView):
    """
    资讯操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def is_request_data_valid(self, **kwargs):
        if 'tags' in kwargs:
            try:
                tags = json.loads(kwargs['tags'])
            except Exception as e:
                return False, e.args
            else:
                if not isinstance(tags, (list, tuple)):
                    return False, 'Tags type error.'
        return True, None

    def get_information_object(self, information_id):
        return Information.get_object(pk=information_id)

    def post(self, request, *args, **kwargs):
        form = InformationInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InformationSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = InformationUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_information_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = InformationSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = InformationDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_information_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InformationSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InformationDetail(generics.GenericAPIView):
    """
    资讯详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_information_detail(self, information_id):
        return Information.get_detail(pk=information_id)

    def post(self, request, *args, **kwargs):
        form = InformationDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_information_detail(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InformationDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InformationList(generics.GenericAPIView):
    """
    资讯详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_information_list(self, **kwargs):
        return Information.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = InformationListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_information_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InformationListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)


class CaseAction(generics.GenericAPIView):
    """
    案例操作
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def is_request_data_valid(self, **kwargs):
        if 'tags' in kwargs:
            try:
                tags = json.loads(kwargs['tags'])
            except Exception as e:
                return False, e.args
            else:
                if not isinstance(tags, (list, tuple)):
                    return False, 'Tags type error.'
        return True, None

    def get_case_object(self, case_id):
        return Case.get_object(pk=case_id)

    def post(self, request, *args, **kwargs):
        form = CaseInputForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CaseSerializer(data=cld)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        form = CaseUpdateForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        is_valid, error_message = self.is_request_data_valid(**cld)
        if not is_valid:
            return Response({'Detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_case_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CaseSerializer(instance)
        try:
            serializer.update(instance, cld)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = CaseDeleteForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        instance = self.get_case_object(cld['id'])
        if isinstance(instance, Exception):
            return Response({'Detail': instance.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CaseSerializer(instance)
        try:
            serializer.delete(instance)
        except Exception as e:
            return Response({'Detail': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CaseDetail(generics.GenericAPIView):
    """
    案例详情
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_case_detail(self, case_id):
        return Case.get_detail(pk=case_id)

    def post(self, request, *args, **kwargs):
        form = CaseDetailForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        detail = self.get_case_detail(cld['id'])
        if isinstance(detail, Exception):
            return Response({'Detail': detail.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CaseDetailSerializer(data=detail)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CaseList(generics.GenericAPIView):
    """
    案例详情列表
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_case_list(self, **kwargs):
        return Case.filter_details(**kwargs)

    def post(self, request, *args, **kwargs):
        form = CaseListForm(request.data)
        if not form.is_valid():
            return Response({'Detail': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        cld = form.cleaned_data
        details = self.get_case_list(**cld)
        if isinstance(details, Exception):
            return Response({'Detail': details.args}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CaseListSerializer(data=details)
        if not serializer.is_valid():
            return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        list_data = serializer.list_data(**cld)
        if isinstance(list_data, Exception):
            return Response({'Detail': list_data.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list_data, status=status.HTTP_200_OK)
