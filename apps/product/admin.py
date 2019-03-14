# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from models import *

# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
   list_display  = [field.name for field in Goods._meta.get_fields()]
   list_display.remove('image')
   list_display += ['get_image']
   def get_image(self,obj):
      color_image = Goods.objects.filter(goods_sn=obj.goods_sn)
      if color_image.exists():
          color_image = color_image[0]
          return mark_safe(u'<img src="%s" width="100px">' % color_image.image.url)
        # color_image 必须是 ImageField类型
      return
   get_image.short_description = u'图片'

class UserPropertyAdmin(admin.ModelAdmin):
    list_display  = ['username','birthday','gender','mobile']

admin.site.register(UserProperty, UserPropertyAdmin)
admin.site.register(Goods, GoodsAdmin)

