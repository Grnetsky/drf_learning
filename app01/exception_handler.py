# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 15:39
# @Author  : Garnetsky
# @FileName: exception_handler.py
# @Software: PyCharm
# @Cnblogs ：http://blog.xroot.top
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

"""
全局异常处理
"""

def my_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # 两种情况，一个是None，drf没有处理
    # response对象，django处理了，但是处理的不符合咱们的要求
    # print(type(exc))
    if not response:
        if isinstance(exc, ZeroDivisionError):
            return Response(data={'status': 777, 'error_msg': "除以0的错误" + str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': 999, 'error_msg': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # return response
        print(response.data)
        return Response(data={'status': 888, 'error_msg': response.data}, status=status.HTTP_400_BAD_REQUEST)