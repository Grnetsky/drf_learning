# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 19:49
# @Author  : Garnetsky
# @FileName: app_permission.py
# @Software: PyCharm
# @Cnblogs ：http://blog.xroot.top
from rest_framework.permissions import BasePermission

from rest_framework.exceptions import PermissionDenied


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 不是超级用户，不能访问
        # 由于认证已经过了，request内就有user对象了，当前登录用户
        user = request.user  # 当前登录用户
        # 如果该字段用了choice，通过get_字段名_display()就能取出choice后面的中文
        if user.is_staff:
            return True
        else:
            # raise PermissionDenied("你没有权限")  # 或者抛出权限异常来自定义提示信息
            return False
