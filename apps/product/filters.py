# -*- coding: utf-8 -*-

import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # pricemin = django_filters.NumberFilter(
    #     field_name='shop_price', help_text="最低价格", lookup_expr='gte')
    #
    # pricemax = django_filters.NumberFilter(
    #     field_name='shop_price', help_text="最高价格", lookup_expr='lte')
    #
    # name = django_filters.CharFilter(
    #     field_name='name',
    #     lookup_expr='icontains',
    #     help_text="商品名称(全局模糊搜索)")
    #
    # top_category = django_filters.NumberFilter(
    #     field_name='category',
    #     method='top_category_filter',
    #     help_text="类目等级:1,2,3")
    #
    # def top_category_filter(self, queryset, name, value):
    #     return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
    #                            Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['name']