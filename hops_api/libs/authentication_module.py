#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:HanFuming

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated
from apps.userAuth import models

# get_token生成加密token,out_token解密token
from libs.token_module import out_token


class TokenAuth(BaseAuthentication):
    # 存储在前端的token解密比对
    def authenticate(self, request):
        token = request.GET.get("token")
        if not token:
            token = request.headers.get("Authorization")
        obj = models.UserToken.objects.filter(token=token).first()
        if obj:
            token_obj = out_token(obj.user.username, token)
            if token_obj:
                return obj.user, None
            else:
                raise NotAuthenticated({"code": 50008, "message": "token已过期"})
        else:
            raise NotAuthenticated("用户未登陆")

