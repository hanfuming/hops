from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from libs.checkCode import md5hash, random_base32
from libs.token_module import get_token
from apps.asset import models
import json


class HostView(APIView):

        def get(self, request, *args, **kwargs):
            response = {"code": None, "data": {"total": None, "items": None}}
            hostList = models.host.objects.all().values("hostId", "hostName", "hostOs", "osVersion", "status",
                                                        "hardwareId__CPU","hardwareId__memory", "disk", "innerIP",
                                                        "outerIP","proId__proName", "cloud", "region", "createTime")
            ret_list = list(hostList)
            response["code"] = 20000
            response["data"]["items"] = ret_list
            response["data"]["total"] = len(ret_list)
            return JsonResponse(response)

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class CdbView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass


class ProductView(APIView):

        def get(self, request, *args, **kwargs):
            response = {"code": None, "data": {"total": None, "items": None}}
            proId = request.query_params.get('proId')
            try:
                if proId:
                    project = models.project.objects.filter(proId=proId).first()
                else:
                    project = models.project.objects.all().values()
                ret_list = list(project)
                response["code"] = 20000
                response["data"]["items"] = ret_list
                response["data"]["total"] = len(ret_list)
                return JsonResponse(response)
            except Exception as e:
                response["code"] = 20001
                return JsonResponse(response)

        def post(self, request, *args, **kwargs):
            response = {"code": None, "message": None}
            req = json.loads(request.body)
            parentId = req.get('parentId')
            proList = [parentId, ]
            f = models.project.objects.filter(parentId=parentId).values("ancestors")
            if f:
                req["ancestors"] = list(f)[0].get("ancestors")
                req["orderNum"] = 1
                req["createBy"] = "admin"
            else:
                l = models.project.objects.filter(proId=parentId).values("ancestors")
                req["ancestors"] = list(l)[0].get("ancestors") + ',' + str(parentId)
                req["orderNum"] = 1
                req["createBy"] = "admin"
            print(req)
            try:
                obj = models.project(**req)
                obj.save()
                response["code"] = 20000
                response["message"] = "项目添加成功"
            except Exception as e:
                response["code"] = 20001
                response["message"] = "项目添加失败"
            return JsonResponse(response)

        def put(self, request, *args, **kwargs):
            response = {"code": 20000, "message": None}
            req = json.loads(request.body)
            print(req)
           # models.project.objects.update(**req)
            return JsonResponse(response)

        def delete(self, request, *args, **kwargs):
            response = {"code": None, "message": None}
            req = json.loads(request.body)
            proId = req.get("proId")
            if models.project.objects.filter(parentId=proId):
                response["code"] = 20001
                response["message"] = "此项目下存在子项目"
            else:
                try:
                    models.project.objects.filter(proId=proId).delete()
                    response["code"] = 20000
                    response["message"] = "项目已删除"
                except Exception as e:
                    response["code"] = 20002
                    response["message"] = "项目删除失败"
            return JsonResponse(response)
