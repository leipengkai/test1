# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status,permissions,filters
from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication,BaseAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.serializers import api_settings
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



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
class GoodsEasyUIViewSet(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'goods.html'

    def get(self, request):
        queryset = Goods.objects.all()
        paginator = Paginator(queryset , 2)
        host = request.META['HTTP_HOST']
        # 参考:https://blog.csdn.net/weixin_42681866/article/details/85010630
        page = request.GET.get('page') # 从查询字符串获取page的当前页数
        if page: # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
            data_list = paginator.page(page).object_list
        else:
            data_list = paginator.page(1).object_list
        try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
        return render(request, "goods.html", {
            'page_object':page_object,
            'data_list':data_list,
            'host':host,
        }) # 返回给模版当前页码对象和当前页码的数据集

        # return Response({'profiles': queryset})

    def easyui(self,request):
        queryset = Goods.objects.all()
        # queryset = Goods.objects.filter(id=pk)[0]
        # images = queryset.images.model.objects.filter(goods=queryset)
        # goods_desc = queryset.goods_desc
        # goods_desc = re.sub('(src=".*?")',r'\1 class="img-responsive"',goods_desc)


        return render(request,'goods.html',{'goods':queryset})

class CustomIndexViewSet(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    @csrf_exempt
    def get(self, request):
        return render(request, "index.html", {})

class CustomLoginViewSet(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return render(request, "index.html", {user:user})
        return render(request, "index.html", {})

