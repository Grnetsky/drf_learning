# -*- coding: utf-8 -*-
# @Time    : 2022/1/29 12:51
# @Author  : Garnetsky
# @FileName: urls.py
# @Software: PyCharm
# @Cnblogs ：http://blog.xroot.top
from django.contrib import admin
from django.urls import path, re_path, include

import app01
from app01 import views
from rest_framework_simplejwt import views as JWTAuthenticationViews

urlpatterns = [
]
from rest_framework import routers

# 第二步：有两个类,实例化得到对象
# routers.DefaultRouter 生成的路由更多
# routers.SimpleRouter
router = routers.DefaultRouter()
# 第三步：注册
# router.register('前缀','继承自ModelViewSet视图类','别名')
router.register('books7', views.Book6ModelView)  # 不要加斜杠了
# 第四步
# router.urls # 自动生成的路由,加入到原路由中
router.register('permission', views.PermissionView)
router.register('user', views.UserView)
router.register('role', views.RoleView)
urlpatterns += router.urls
