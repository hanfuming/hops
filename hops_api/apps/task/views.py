from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from libs.checkCode import md5hash, random_base32
from libs.token_module import get_token
from apps.asset import models
from libs import saltapi
import json


class ExecuteView(APIView):

        def get(self, request):
            pass

        def post(self, request, *args, **kwargs):
            response = {"code": None, "message": None, "data": None}
            salt_info = {"url": "https://193.112.46.157:8000/", "token": "c128f133b1bee34b3edbc485f686dcc263644887"}
            sapi = saltapi.SaltAPI(url=salt_info["url"], token=salt_info["token"])
            req = json.loads(request.body)
            execute_host = req.get("execute_host")
            execute = req.get("execute")
            try:
                jid = sapi.salt_command(tgt=execute_host, fun='cmd.run', arg=execute)
                response["code"] = 20000
                response["message"] = "执行成功"
                response["data"] = str(jid)
            except Exception as e:
                response["code"] = 20001
                response["message"] = "执行失败"
                response["data"] = str(e)
            return JsonResponse(response)

        def put(self, request):
            pass

        def delete(self, request):
            pass


class FileView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class DeployView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class JobView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class CronView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class ScriptView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass