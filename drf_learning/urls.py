"""drf_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

import app01
from app01 import views
from rest_framework_simplejwt import views as JWTAuthenticationViews

urlpatterns = [
    # 进行登录身份验证
    path('api/token/', JWTAuthenticationViews.TokenObtainPairView.as_view()),
    # 刷新身份令牌
    path('api/token/refresh/', JWTAuthenticationViews.TokenRefreshView.as_view()),

    path('admin/', admin.site.urls),
    re_path('books/(?P<pk>\d+)', views.BookView.as_view()),
    path('books/', views.BookView.as_view()),

    path('books2/', views.Book2View.as_view()),
    re_path('books2/(?P<pk>\d+)', views.Book2DetailView.as_view()),

    path('books3/', views.Book3View.as_view()),
    re_path('books3/(?P<pk>\d+)', views.Book3DetailView.as_view()),

    path('books4/', views.Book4View.as_view()),
    re_path('books4/(?P<pk>\d+)', views.Books4View.as_view()),

    #  viewseturl
    path('books5/', views.Book5ViewSet.as_view(actions={'get': 'list'})),
    re_path('books5/(?P<pk>\d+)', views.Book5ViewSet.as_view(actions={'get': 'retrieve'})),

    # TODO 推荐用法
    path('books6/', views.Book6ViewSet.as_view(actions={'get': 'list'})),
    re_path('books6/(?P<pk>\d+)', views.Book6ViewSet.as_view(actions={'get': 'retrieve'})),
    path('api/', include('app01.urls'))

    # 使用ModelViewSet编写5个接口
    # path('books7/', views.Book6ModelView.as_view(actions={'get':'list','post':'create'})), #当路径匹配，又是get请求，会执行Book5View的list方法
    # re_path('books7/(?P<pk>\d+)', views.Book6ModelView.as_view(actions={'get':'retrieve','put':'update','delete':'destroy'}))
]

"""
使用了ModelViewSet时可以这么配路由

相当于加了
^books/$    name: book-list
^books/{pk}/$   name: book-detail


访问时记得最后一定要加'/'
"""
# 第一步：导入routers模块
