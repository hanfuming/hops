from django.db import models


class UserInfo(models.Model):
    username = models.CharField("用户账号", max_length=32)
    password = models.CharField("用户密码", max_length=64)
    nickName = models.CharField("用户昵称", max_length=64, null=True)
    mobile = models.CharField("手机号", max_length=20, null=True)
    email = models.CharField("邮箱", max_length=64, null=True)
    sex = models.CharField("用户性别（0男 1女 2未知", max_length=1, default='0')
    avatar = models.CharField("头像地址", max_length=100, null=True)
    status = models.CharField("用户状态(0正常,1停用)", max_length=1, default='0')
    delFlag = models.CharField("删除标识(0存在,1删除)", max_length=1, default='0')
    createTime = models.DateTimeField("创建时间", auto_now_add=True)
    loginTime = models.DateTimeField("登录时间", auto_now=True)
    LastLoginTime = models.DateTimeField("最后时间", auto_now=True)
    loginIP = models.CharField("登录IP", max_length=16, null=True)
    count = models.IntegerField("登录次数", null=True)
    remark = models.CharField("备注", max_length=200, null=True)
    roles = models.ForeignKey("Role", on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "用户信息表"


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Role(models.Model):
    roleName = models.CharField("角色名称", max_length=32)
    roleKey = models.CharField("角色权限字符串", max_length=100)
    status = models.CharField("角色状态(0正常,1停用)", max_length=1, default='0')
    delFlag = models.CharField("删除标识(0存在,1删除)", max_length=1, default='0')
    createTime = models.DateTimeField("创建时间", auto_now_add=True)
    createBy = models.CharField("创建者", max_length=32, default=None)
    updateTime = models.DateTimeField("更新时间", auto_now=True)
    updateBy = models.CharField("更新者", max_length=32, default=None)
    remark = models.CharField("备注", max_length=200, null=True)

    def __str__(self):
        return self.roleKey

    class Meta:
        verbose_name_plural = "角色表"


class Menu(models.Model):
    menuName = models.CharField("菜单名称", max_length=50)
    parentId = models.IntegerField("父菜单ID", default=0)
    orderNum = models.IntegerField("显示顺序", default=0)
    path = models.CharField("路由地址", max_length=200, default=None)
    component = models.CharField("组件路径", max_length=255, default=None)
    isFrame = models.IntegerField("是否为外链(0是 1否)", default=1)
    menuType = models.CharField("菜单类型（M目录 C菜单 F按钮）", max_length=1, default=None)
    hidden = models.CharField("菜单显示状态（0显示 1隐藏）", max_length=1, default='0')
    perms = models.CharField("权限标识", max_length=100, default=None)
    icon = models.CharField("菜单图标", max_length=100, default='#')
    createTime = models.DateTimeField("创建时间", auto_now_add=True)
    createBy = models.CharField("创建者", max_length=32, default=None)
    updateTime = models.DateTimeField("更新时间", auto_now=True)
    updateBy = models.CharField("更新者", max_length=32, default=None)
    remark = models.CharField("备注", max_length=200, null=True)
    role = models.ManyToManyField("Role")

    def __str__(self):
        return self.menuName

    class Meta:
        verbose_name_plural = "菜单表"
