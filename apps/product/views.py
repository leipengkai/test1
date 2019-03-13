# -*- coding: utf-8 -*-

from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status,permissions,filters
from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication,BaseAuthentication
# from django_filters.rest_framework import DjangoFilterBackend


from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from models import UserProperty,Goods
from serializers import UserRegSerializer,UserDetailSerializer,GoodsSerializer
from tasks import django_send_email,longtime_test

# from filters import GoodsFilter

from django.db.models import Q


# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, mobile=None,**kwargs):
        try:
            user = UserProperty.objects.get(username=username)
            if user.check_password(password):
                print('准备celery发送邮件')
                msg = "<p>您已成功登录平台,谢谢您的使用</p>"
                django_send_email(email=user.email, msg=msg)
                return user
            else:
                print('用户验证失败')
                return None
        except Exception as e:
            return None


class UserViewset(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = UserProperty.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "list":
            return []
            # return [permissions.IsAdminUser]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        data = request.data
        mobile = data.get('mobile')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.set_password(user.password)
        user.mobile = mobile
        user.save()

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["mobile"] = mobile


        headers = self.get_success_headers(serializer.data)
        return Response(
            re_dict,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class GoodsViewSet(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = []
    filter_backends = (
        # DjangoFilterBackend,
        filters.SearchFilter,
        # filters.OrderingFilter,
    )
    search_fields = ('name', 'key')
    # filter_class = GoodsFilter



class GoodsAdminViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    search_fields = ('name', 'key')
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    filter_backends = (
        # DjangoFilterBackend,
        filters.SearchFilter,
        # filters.OrderingFilter,
    )
    search_fields = ('name', 'key')
    # filter_class = GoodsFilter
