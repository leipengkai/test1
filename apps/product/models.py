# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Goods(models.Model):

    """
    商品
    """

    goods_sn = models.IntegerField(
        primary_key=True, verbose_name="pk")
    name = models.CharField(max_length=100, verbose_name="商品名")
    key = models.CharField(max_length=100, verbose_name="商品搜索关键词")
    image = models.ImageField(max_length=200, upload_to="goods_image/",verbose_name="商品图片")
    priority = models.IntegerField(default=0, verbose_name="产品优先级")
    file_address = models.CharField(max_length=100, verbose_name="文件地址")


    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品' # 防止admin中app下的Model名，出现中文乱码

    def __str__(self):
        return self.name

class UserProperty(AbstractUser):
    """
    用户
    """

    username = models.CharField(
        max_length=30,
        null=True,
        blank=True,unique=True,
        verbose_name="姓名")

    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(
        ("male", u"男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(
        null=True,
        blank=True,
        max_length=11,
        verbose_name="电话")
    image = models.ImageField(upload_to='users_avatar', verbose_name='用户头像', default='')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
