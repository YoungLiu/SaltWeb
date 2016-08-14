#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json
import platform

import salt
import salt.key
import salt.version

from main import *


# 管理中心
class Dashboard:
    @Check_Login
    def GET(self):
        sData = getLogin()
        #SID = sData['SID']
        #ShowName = sData['ShowName']
        #print sData
        #print "ShowName: " + ShowName

        LocalData = {
            'uptime': 2016,
            'ip': "This is a test IP",
            'hostname':platform.node(),
            'os':"This is a test os",
            'disk_all':12,
            'disk_free':12,
            'disk_used':12,
            'disk_used_p':12,
            'loadavg_1':12,
            'loadavg_5':12,
            'loadavg_15':12,
            'salt_version':salt.version.__version__,
            'mem_total':1024,
            'mem_free':1000,
            'mem_used':24,
            'mem_used_p':0.24,
            'net_in':99,
            'net_out':99,
            'cpu_physical_num':4,
            'cpu_logical_cores':8,
            'process_num':16,
            'login_user_num':1,
            'cpu_percent':0.98,
            'Manufacturer':"",
            'Product_Name':"",
        }
        return render.dashboard(MyData=sData,LD=LocalData)

# 首页加载数据
class IndexData:
    def salt_minions(self):
        __opts__ = salt.config.client_config('/etc/salt/master')
        mykey = salt.key.Key(__opts__)
        K = mykey.list_keys()
        keys_ok = len(K['minions'])
        keys_rej = len(K['minions_rejected'])
        keys_pre = len(K['minions_pre'])
        local = salt.client.LocalClient()
        rt = local.cmd('*','test.ping',timeout=1)
        minions_online = len(rt)
        sm = {'keys_ok':keys_ok, 'keys_rej':keys_rej, 'keys_pre':keys_pre, 'online':minions_online, 'offline':keys_ok-minions_online}
        return sm

    @Check_Login
    def GET(self):
        rt_data = {}
        rt_data.update(self.salt_minions())
        web.header('content-type','text/json')
        return json.dumps(rt_data)

# 选项管理
class Options:
    def GET(self):
        if getLogin():
            sData = getLogin()
            SID = sData['SID']
            ShowName = sData['ShowName']
            #print sData
            #print "ShowName: " + ShowName
            #return render.options(ShowName=ShowName,uid=SID)
            g = db.query('''select * from options order by type,value''')
            #op = db.query('''select * from options where type="option"''')
            OpsData = []
            SelectType = []
            for i in g:
                if str(i.type) == 'option':
                    SelectType.append({'value':i.value,'comment':i.comment})
                OpsData.append({'id':i.id,'type':i.type,'value':i.value,'comment':i.comment,'status':i.status})
            #for i in op:
            #    SelectType.append({'value':i.value,'comment':i.comment})
            return render.options(ShowName=ShowName,uid=SID,OpsData=OpsData,SelectType=SelectType)
        else:
            web.setcookie('HTTP_REFERER', web.ctx.fullpath, 86400)
            return web.seeother("/login")

    def POST(self):
        if getLogin() is False:
            web.ctx.status = '401 Unauthorized'
            return '401 - Unauthorized\n'
        i = web.input()
        OpsID = i.id
        OpsType = i.type
        OpsValue = i.value
        OpsComment = i.comment
        OpsStatus = i.status
        #print "Ops: " + OpsType + OpsValue
        if OpsID == "none":
            db.query('''insert into options(type,value,comment,status)values("%s","%s","%s","%s")''' % (OpsType,OpsValue,OpsComment,OpsStatus))
        else:
            db.query('''update options set type="%s",value="%s",comment="%s",status="%s" where id="%s"''' % (OpsType,OpsValue,OpsComment,OpsStatus,OpsID))
        return web.seeother("/admin/options")
        #return render('alert("操作成功！");window.location.href="/admin/options";')
