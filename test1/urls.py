# -*- coding: utf-8 -*-
from jet.dashboard.dashboard_modules import google_analytics_views

from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.conf.urls.static import static

from product.views import UserViewset,GoodsViewSet, GoodsAdminViewSet, GoodsEasyUIViewSet,\
    CustomLoginViewSet, CustomIndexViewSet

from .settings import MEDIA_ROOT,STATIC_ROOT

router = DefaultRouter()

router.register(r'users', UserViewset, base_name="users")
router.register(r'goods', GoodsViewSet, base_name="goods")
# router.register(r'easyui', GoodsEasyUIViewSet, base_name="easyui")
router.register(r'admin/goods', GoodsAdminViewSet, base_name="admin_goods")

urlpatterns = [
    # Examples:
    # url(r'^$', 'test1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^api/v1/', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    url(r'^easyui/$', GoodsEasyUIViewSet.as_view()),
    url(r'^index/$', CustomIndexViewSet.as_view()),
    url(r'^login/$', CustomLoginViewSet.as_view()),

]
