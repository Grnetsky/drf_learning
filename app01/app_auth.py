# -*- coding: utf-8 -*-
# @Time    : 2022/1/26 21:47
# @Author  : Garnetsky
# @FileName: app_auth.py
# @Software: PyCharm
# @Cnblogs ：http://blog.xroot.top

"""
这是认证组件的代码
"""

# 写一个认证类 app_auth.py
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from app01.models import UserToken
#
#
# class MyAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         # 认证逻辑，如果认证通过，返回两个值
#         # 如果认证失败，抛出AuthenticationFailed异常
#         token = request.GET.get('token')
#         if token:
#             user_token = UserToken.objects.filter(token=token).first()
#             # 认证通过
#             if user_token:
#                 return user_token.user, token
#             else:
#                 raise AuthenticationFailed('认证失败')
#         else:
#             raise AuthenticationFailed('请求地址中需要携带token')
#

""" djangorestframework-simplejwt进行身份验证"""
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
