from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from libs.checkCode import md5hash, random_base32
from libs.token_module import get_token
from apps.userAuth import models
import json


class LoginView(APIView):
    """用户登录"""
    authentication_classes = []

    def post(self, request):
        response = {"code": 20000, "message": None, "data": {"name": None, "token": None}}
        try:
            name = request.data.get("username")
            pwd = md5hash(request.data.get("password"))
            user = models.UserInfo.objects.filter(username=name, password=pwd).first()
            if user:
                token = get_token(name, 3600)    # 将name进行加密,3600设定超时时间
                models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
                response["message"] = "登入成功"
                response["data"]["token"] = token
                response["data"]["name"] = user.username
            else:
                response["code"] = 20001
                response["message"] = "用户名或密码错误"
        except Exception as e:
                print(e)
                response["code"] = 20002
                response["message"] = "请求异常"

        return JsonResponse(response)


class LogoutView(APIView):

    def post(self, request):
        response = {"code": 20000, "message": None}
        token = request.headers.get("Authorization")
        try:
           models.UserToken.objects.filter(token=token).update(token="null")
           response["message"] = "已退出登录"
        except Exception as e:
           response["code"] = 20001
           response["message"] = "未退出登录"

        return JsonResponse(response)


class UserInfoView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": 20000, "permissions": None, "roles": None, "user": None}
        token = request.headers.get("Authorization")
        obj = models.UserToken.objects.filter(token=token).values("user__username", "user__nickName", "user__avatar", "user__roles__roleKey").first()
        items = {"name": obj["user__username"],
                 "nickName": obj["user__nickName"],
                 "avater": obj["user__avatar"],
                 "roles": obj["user__roles__roleKey"]}
        if obj["user__roles__roleKey"] == "admin":
            response["permissions"] = ["*:*:*"]
        else:
            perms = models.Role.objects.filter(roleKey=obj["user__roles__roleKey"]).all().values("menu__perms")
            perms_list = []
            for v in perms:
                perms_list.append(v["menu__perms"])
            response["permissions"] = perms_list
        response["roles"] = obj["user__roles__roleKey"]
        response["user"] = items
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        response = {"code": 20000, "message": None}
        req = json.loads(request.body)
        username = req.get("username")
        oldpwd = md5hash(req.get("password"))
        newpwd = md5hash(req.get("newPassword"))
        if models.UserInfo.objects.filter(username=username, password=oldpwd).filter():
            try:
                models.UserInfo.objects.filter(username=username).update(password=newpwd)
                response["message"] = "密码修改成功"
            except Exception as e:
                response["message"] = "密码修改失败"
        else:
            response["message"] = "密码错误"
        return JsonResponse(response)


class UserManageView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": None, "data": {"total": None, "items": None}}
        userId = request.query_params.get('userId')
        if userId:
            uList = models.UserInfo.objects.filter(id=userId).values("username", "nickName", "roles__roleName", "mobile", "status", "createTime")
        else:
            uList = models.UserInfo.objects.all().values("username", "nickName", "roles__roleName", "mobile", "status", "createTime")
        ret_list = list(uList)
        response["code"] = 20000
        response["data"]["items"] = ret_list
        response["data"]["total"] = len(ret_list)
        return JsonResponse(response)

    def post(self, request, *args, **kwargs):
        response = {"code": 20000, "message": None}
        req = json.loads(request.body)
        username = req.get("username")
        roles_id = req.get("roles_id")
        pwd = random_base32()
        password = md5hash(pwd)
        req["password"] = password
        try:
            obj = models.UserInfo(**req)
            obj.save()
            response["msmessageg"] = "用户添加成功"
            # email.sendmail("819121281@qq.com",pwd)
        except Exception as e:
            print(e)
            response["code"] = 20001
            response["message"] = "用户添加失败"
        return JsonResponse(response)

    def delete(self, request, *args, **kwargs):
        response = {"code": 20000, "message": None}
        req = json.loads(request.body)
        userName = req.get("username")
        if userName == "admin":
            response["code"] = 20001
            response["message"] = "系统用户不能被删除"
        else:
            try:
                models.UserInfo.objects.filter(username=userName).delete()
                response["message"] = "用户删除成功"
            except Exception as e:
                response["code"] = 20002
                response["message"] = "用户删除失败"
        return JsonResponse(response)


class roleManageView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": None, "data": {"total": None, "items": None}}
        uList = models.Role.objects.all().values("id", "roleName", "roleKey", "status")
        ret_list = list(uList)
        response["code"] = 20000
        response["data"]["items"] = ret_list
        response["data"]["total"] = len(ret_list)
        return JsonResponse(response)

    def post(self, request, *args, **kwargs):
        response = {"code": 20000, "message": None}
        req = json.loads(request.body)
        roleName = req.get("roleName")
        roleKey = req.get("roleKey")
        token = request.headers.get("Authorization")
        createBy = models.UserToken.objects.filter(token=token).values("user__username")
        menuIds = req.get("menuIds")
        try:
            obj = models.Role.objects.create(roleName=roleName, roleKey=roleKey, createBy=createBy, updateBy=createBy)
            role__obj = models.Role.objects.get(roleKey=roleKey)
            menu__obj = models.Menu.objects.filter(id__in=menuIds)
            role__obj.menu_set.add(*menu__obj)
            response["message"] = "角色添加成功"
        except Exception as e:
            print(e)
            response["code"] = 20001
            response["message"] = "角色添加失败"
        return JsonResponse(response)

    def delete(self, request, *args, **kwargs):
        response = {"code": 20000, "message": None}
        req = json.loads(request.body)
        roleId = req.get("roleId")
        if roleId == "1":
            response["code"] = 20001
            response["message"] = "管理员角色不能被删除"
        else:
            try:
                models.Role.objects.filter(id=roleId).delete()
                response["message"] = "角色删除成功"
            except Exception as e:
                response["code"] = 20002
                response["message"] = "角色删除失败"
        return JsonResponse(response)


def convertToTreeData(data, pid):
    result = []
    i = 0
    while(i < len(data)):
        if (data[i]["parentId"] == pid):
            obj = {
                "path": data[i]["path"],
                "component": data[i]["component"],
                "hidden": data[i]["hidden"],
                "name": data[i]["path"],
                "meta": {"title": data[i]["menuName"], "icon": data[i]["icon"]}
            }
            temp = convertToTreeData(data, data[i]["id"])
            if (len(temp) > 0):
                obj["children"] = temp
            result.append(obj)
        i = i+1
    return result


def menuToTreeData(data, pid):
    result = []
    i = 0
    while(i < len(data)):
        if (data[i]["parentId"] == pid):
            obj = {
                "id": data[i]["id"],
                "label": data[i]["menuName"]
            }
            temp = menuToTreeData(data, data[i]["id"])
            if (len(temp) > 0):
                obj["children"] = temp
            result.append(obj)
        i = i+1
    return result


class RoutesView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": 20000, "datail": None}
        roles = request.query_params.get('roles')
        obj = models.Menu.objects.filter(role__roleKey=roles, menuType__in=('M', 'C')).values()
        routes = convertToTreeData(obj, 0)
        response["datail"] = routes
        return JsonResponse(response)


class roleMenusView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": 20000, "datail": None}
        obj = models.Menu.objects.all().values()
        response["datail"] = list(obj)
        return JsonResponse(response)


class menuTreeView(APIView):

    def get(self, request, *args, **kwargs):
        response = {"code": 20000, "data": None}
        roleId = request.query_params.get('roleId')
        if roleId:
            role__obj = models.Role.objects.get(id=roleId)
            obj = role__obj.menu_set.all().values()
        else:
            obj = models.Menu.objects.all().values()
        routes = menuToTreeData(obj, 0)
        response["data"] = routes
        return JsonResponse(response)

