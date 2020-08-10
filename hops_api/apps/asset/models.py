from django.db import models
import django.utils.timezone as timezone


class project(models.Model):
    proId = models.AutoField('项目id', primary_key=True)
    parentId = models.IntegerField('父项目id')
    ancestors = models.CharField('祖级列表', max_length=50)
    proName = models.CharField('项目名称', max_length=50)
    orderNum = models.IntegerField('显示顺序')
    leader = models.CharField('负责人', max_length=20)
    phone = models.CharField('联系电话', max_length=11)
    email = models.CharField('邮箱', max_length=50)
    status = models.CharField('项目状态（0正常 1已下线 2测试中）', max_length=1)
    createBy = models.CharField('创建人', max_length=64)
    createTime = models.DateTimeField('创建时间', default=timezone.now)


class hardware(models.Model):
    hardwareId = models.AutoField('硬件ID', primary_key=True)
    CPU = models.IntegerField('cpu')
    memory = models.IntegerField('内存')


class host(models.Model):
    hostId = models.AutoField('主机ID', primary_key=True)
    proId = models.ForeignKey('project', to_field='proId', on_delete=models.SET_DEFAULT, default='999')
    hostName = models.CharField('主机名称', max_length=50)
    hostOs = models.CharField('主机系统', max_length=20)
    osVersion = models.CharField('系统版本', max_length=20)
    hardwareId = models.ForeignKey('hardware', to_field='hardwareId', on_delete=models.DO_NOTHING)
    disk = models.IntegerField('磁盘',)
    innerIP = models.CharField('内网IP', max_length=16)
    outerIP = models.CharField('外网IP', max_length=16)
    cloud = models.CharField('所属云', max_length=60)
    region = models.CharField('所属区域', max_length=60)
    status = models.CharField('主机状态（0正常 1已下线 2故障）', max_length=1)
    createTime = models.DateTimeField('创建时间')
    remark = models.CharField('备注', max_length=128)
