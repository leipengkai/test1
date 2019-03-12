# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from models import UserProperty,Goods


class UserRegSerializer(serializers.ModelSerializer):

    mobile = serializers.CharField(max_length=11)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=UserProperty.objects.all())])

    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=UserProperty.objects.all(),
                message="用户已经存在")])

    password = serializers.CharField(
        style={
            'input_type': 'password'},
        help_text="密码",
        label="密码",
        write_only=True,
    )
    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if UserProperty.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

    class Meta:
        model = UserProperty
        fields = ("username", "mobile" ,'password','email')

class UserDetailSerializer(serializers.ModelSerializer):

        class Meta:
            model = UserProperty
            fields = ("username", "gender", "birthday", "email", "mobile","id")

class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ("goods_sn", "name", "key", "image", "priority","file_address")
