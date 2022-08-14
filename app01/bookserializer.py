# -*- coding: utf-8 -*-
# @Time    : 2022/1/24 23:57
# @Author  : Garnetsky
# @FileName: bookserializer.py
# @Software: PyCharm
# @Cnblogs ：http://blog.xroot.top
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app01.models import User, Permissions, Role
from app01.views import Book


# 定义校验函数
def check_author(data):
    if data.startswith('sb'):
        raise ValidationError('作者名字不能以sb开头')
    else:
        return data


class BookSerializer(serializers.Serializer):
    # id=serializers.CharField()
    name = serializers.CharField(max_length=16, min_length=4)
    # price=serializers.DecimalField()
    price = serializers.CharField()
    author = serializers.CharField(validators=[check_author])  # validators=[] 列表中写函数内存地址
    publish = serializers.CharField()

    # 或者也可以这么定义校验函数
    def validate_price(self, data):  # validate_字段名  接收一个参数
        # 如果价格小于10，就校验不通过
        # print(type(data))
        # print(data)
        if float(data) > 10:
            return data
        else:
            # 校验失败，抛异常
            raise ValidationError('价格太低')

    # 或者调用全局效验方法
    def validate(self, validate_data):  # 全局钩子
        print(validate_data)
        author = validate_data.get('author')
        publish = validate_data.get('publish')
        if author == publish:
            raise ValidationError('作者名字跟出版社一样')
        else:
            return validate_data

    # 需要重写update方法 告诉框架 哪个数据和哪个字段对应
    def update(self, instance, validated_data):
        # instance是book这个对象
        # validated_data是校验后的数据
        instance.name = validated_data.get('name')
        instance.price = validated_data.get('price')
        instance.author = validated_data.get('author')
        instance.publish = validated_data.get('publish')
        instance.save()  # book.save()   django 的orm提供的
        return instance

    # ser.py 序列化类重写create方法
    # 调用create
    def create(self, validated_data):
        instance = Book.objects.create(**validated_data)
        return instance


"""上面通过继承serializers.Serializers类来实现了数据的增删改查，其中需要自定义需要序列化的字段，还要自己重写update和create方法
很明显，比较有局限性，对于重复的操作没有进行任何包装，增加了代码的复杂度（但是给了用户最大的自由操作数据）


下面介绍serializers.ModelSerializers类
下面几行代码实现了上面几乎所有功能
ModelSerializer 不需要自己写字段，直接使用模型字段，并且不需要自己写update和create方法，其他功能与serializer类一样，（效验）
"""


class BookModelSerializer(serializers.ModelSerializer):  # 继承serializers.ModelSerializers
    class Meta:
        model = Book  # 对应上models.py中的模型
        fields = '__all__'  # 序列化所有字段
        # fields=('name','price','id','author') # 只序列化指定的字段
        # exclude=('name',) #跟fields不能都写，写谁，就表示排除谁
        # read_only_fields=('price',)
        # write_only_fields=('id',) #弃用了，使用extra_kwargs
        extra_kwargs = {  # 类似于这种形式name=serializers.CharField(max_length=16,min_length=4)
            'price': {'write_only': True},
        }

    def validate_price(self, data):  # validate_字段名  接收一个参数
        # 如果价格小于10，就校验不通过
        # print(type(data))
        # print(data)
        if float(data) > 10:
            return data
        else:
            # 校验失败，抛异常
            raise ValidationError('价格太低')


from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        """自动序列化连表，序列化深度设为1"""
        depth = 2

    def validate_username(self, data):
        if data.startswith('sb'):
            raise ValidationError('敏感词汇')
        else:
            return data

    def validate_password(self, data):
        if len(data) <= 8:
            raise ValidationError('密码设置太短')
        else:
            data = make_password(data)
            return data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField()

    class Meta:
        model = Role
        fields = "__all__"
        depth = 1
