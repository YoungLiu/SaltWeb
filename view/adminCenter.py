#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json
import platform

import salt
import salt.key
import salt.version

from main import *
from saltapi import saltwrapper


# 管理中心
class Dashboard:
    @Check_Login
    def GET(self):
        sData = getLogin()
        #SID = sData['SID']
        #ShowName = sData['ShowName']
        #print sData
        #print "ShowName: " + ShowName

        # construct the data of dashboard
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
        saltuser = saltwrapper.user_session()
        saltuser.set_auth_token()
        testJsonData = saltwrapper.test_target(saltuser.auth_token, "*")
        dictMinion = testJsonData["return"][0]
        minions_online = 0
        for minion in dictMinion:
            if dictMinion[minion] == True:
                minions_online += 1
        sm = {'keys_ok':keys_ok, 'keys_rej':keys_rej, 'keys_pre':keys_pre, 'online':minions_online, 'offline':keys_ok-minions_online}
        return sm

    @Check_Login
    def GET(self):
        rt_data = {}
        rt_data.update(self.salt_minions())
        web.header('content-type','text/json')
        return json.dumps(rt_data)

