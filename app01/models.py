from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.CharField(max_length=32)
    publish = models.CharField(max_length=32)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name
        ordering = ['id', 'name']


"""
使用django内置用户系统,drf-simplejwt的认证也是基于这个用户模型的
"""


# RBAC模型
class Permissions(models.Model):
    permission_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.permission_name


class Role(models.Model):
    role_name = models.CharField(max_length=10)
    permission = models.ManyToManyField(Permissions, verbose_name="权限",related_name="permission")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role_name


# 我们重写用户模型类, 继承自 AbstractUser
class User(AbstractUser):
    """自定义用户模型类"""
    # 在用户模型类中增加 mobile 字段
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    role = models.ManyToManyField(Role, verbose_name="角色",related_name="role")

    # 对当前表进行相关设置:
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.username


