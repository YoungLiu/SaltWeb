#!/usr/bin/env python
# -*- coding:utf-8 -*-
import glob

from main import *


# 获取适配hosts的select选项菜单值
def getOptions():
    sd = {'type': []}
    sd['type'].append({"value": "JobManager"})
    sd['type'].append({"value": "RedisData"})
    sd['type'].append({"value": "LogManager"})
    sd['type'].append({"value": "AuthManager"})
    sd['type'].append({"value": "ApiGateway"})
    return sd


# device管理
class Index:
    def GET(self):
        if getLogin():
            SID = getLogin()['SID']
            ShowName = getLogin()['ShowName']
            try:
                # 暂时从数据库中提取device数据,正常应该从bus获取
                getdevices = db.query('''
                                    select d.id,d.devicename,d.devicetype,d.hostip,d.status,d.startdate
                                    from devices as d
                                    ''')
            except:
                # return "服务器(数据库)错误"
                return "Database Error"
            # print getdevices
            return render.hosts(ShowName=ShowName, uid=SID, getHosts=getdevices, sortShow=getOptions())
        else:
            web.setcookie('HTTP_REFERER', web.ctx.fullpath, 86400)
            return web.seeother("/login")


# 模板管理
class Template:
    def GET(self):
        if getLogin():
            Content = {}
            SID = getLogin()['SID']
            ShowName = getLogin()['ShowName']
            path = "/srv/salt/"
            try:
                # 扫面当前salt file server内部的文件
                g = glob.glob(path + 'template_*')
                for filename in g:
                    file = open(filename, "r")
                    content = file.read()
                    Content[filename] = content
                    file.close()
            except Exception, e:
                print Exception, ":", e
                return "Error"
            return render.templates(ShowName=ShowName, uid=SID, getTemplates=Content)
        else:
            web.setcookie('HTTP_REFERER', web.ctx.fullpath, 86400)
            return web.seeother("/login")


# 编辑template
class EditTemplate:
    def POST(self):
        if getLogin() is False:
            web.ctx.status = '401 Unauthorized'
            return '401 - Unauthorized\n'
        p = web.input()
        path = "/srv/salt/"
        try:
            f = open(p.templatename, "w")
            f.write(p.templatecontent)
            f.close()
        except Exception, e:
            print Exception, ":", e
            return "Error"
        return "Edit.True"

# 添加device
class Add:
    @Check_Login
    def GET(self):
        SID = getLogin()['SID']
        ShowName = getLogin()['ShowName']
        # print "ShowName: " + ShowName
        sd = getOptions()
        if sd:
            return render.hostAdd(ShowName=ShowName, uid=SID, SD=sd)
        else:
            return "Options Error! You may check MySQL server ..."

    def POST(self):
        if getLogin() is False:
            web.ctx.status = '401 Unauthorized'
            return '401 - Unauthorized\n'
        p = web.input()
        # 主机名的冲突检测
        try:
            getSQL = db.query(
                '''select devicename from devices where devicename="%s"''' % (p.devicename))
        except Exception, e:
            print "MySQL Error: ", Exception, ":", e
            return "Error"
        if getSQL:
            for i in getSQL:
                if p.devicename == i.devicename:
                    # 主机名冲突
                    return "HostnameError"
        # FIXME:此处首先应当调用Salt API部署相关Device,然后在插入数据


        # 开始插入数据
        try:
            db.query('''
                     insert into
                     devices (devicename,devicetype,hostip,status,startdate)
                     values ("%s","%s","%s","%s",now())
                     ''' %
                     (p.devicename, p.devicetype, p.deviceip, "Online"))
        except Exception, e:
            # 无法提交，可能是数据库挂了
            print "MySQL Error: ", Exception, ":", e
            return "Error"
        # 添加成功
        return "Add.True"


# 编辑device
class Edit:
    def GET(self):
        if getLogin():
            SID = getLogin()['SID']
            ShowName = getLogin()['ShowName']
            # print "ShowName: " + ShowName
            i = web.input()
            pid = i.pid
            sd = getOptions()
            hd = db.query('''select * from hosts where id="%s"''' % pid)
            h = hd[0]
            HostData = {"id": h.id, "hostname": h.hostname, "priip1": h.priip1, "priip2": h.priip2, "pubip1": h.pubip1,
                        "pubip2": h.pubip2, "adminip": h.adminip, "model": h.model, "cpu": h.cpu, "hdd": h.hdd,
                        "mem": h.mem, "os": h.os, "rnum": h.rnum, "storagedate": h.storagedate,
                        "startdate": h.startdate, "role": h.role, "type": h.type, "idc": h.idc, "idctag": h.idctag,
                        "stag": h.stag, "snum": h.snum, "status": h.status, "comment": h.comment}
            # print "HostData: ",HostData
            return render.hostEdit(ShowName=ShowName, uid=SID, SD=sd, HostData=HostData)
        else:
            web.setcookie('HTTP_REFERER', web.ctx.fullpath, 86400)
            return web.seeother("/login")

    def POST(self):
        if getLogin() is False:
            web.ctx.status = '401 Unauthorized'
            return '401 - Unauthorized\n'
        p = web.input()
        # 主机名和内网IP地址1的冲突检测
        try:
            getSQL = db.query(
                '''select id,hostname,priip1 from hosts where hostname="%s" or priip1="%s"''' % (p.hostname, p.priip1))
        except Exception, e:
            print "MySQL Error: ", Exception, ":", e
            return "Error"
        if getSQL:
            for i in getSQL:
                if str(p.id) != str(i.id):
                    # 首先排除对比自身的数据
                    if p.hostname == i.hostname:
                        # 主机名冲突
                        return "HostnameError"
                    if p.priip1 == i.priip1:
                        # 内网IP1冲突
                        return "PriIP1Error"
        # 开始更新数据
        try:
            db.query('''
                     update hosts
                     set hostname="%s",role="%s",priip1="%s",priip2="%s",pubip1="%s",pubip2="%s",model="%s",cpu="%s",hdd="%s",mem="%s",os="%s",rnum="%s",storagedate="%s",adminip="%s",type="%s",startdate="%s",idc="%s",idctag="%s",snum="%s",stag="%s",status="%s",comment="%s",editor="%s",mdate=now()
                     where id="%s"
                     ''' %
                     (p.hostname, p.role, p.priip1, p.priip2, p.pubip1, p.pubip2, p.model, p.cpu, p.hdd, p.mem, p.os,
                      p.rnum, p.storagedate, p.adminip, p.type, p.startdate, p.idc, p.idctag, p.snum, p.stag, p.status,
                      p.comment, getLogin()['SID'], p.id))
        except Exception, e:
            # 无法提交，可能是数据库挂了
            print "MySQL Error: ", Exception, ":", e
            return "Error"
        # 添加成功
        return "Edit.True"
