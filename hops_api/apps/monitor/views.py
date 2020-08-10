from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from libs.checkCode import md5hash, random_base32
from libs.token_module import get_token
from apps.asset import models
import json


class DashboardView(APIView):

        def get(self, request):
            pass

        def post(self, request):
            pass

        def put(self, request):
            pass

        def delete(self, request):
            pass