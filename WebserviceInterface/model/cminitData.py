# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys

from model.__cmdbinit__ import cmetadata, cmdeclarativeBase, CMDBSession

from model.Practicalusing.UnifiedURL import UnifiedURL
from model.Practicalusing.unifiedDnsIp import UnifiedDNSIP
from model.Practicalusing.URLtoDNS import URLtoDNS
from model.Practicalusing.SplicingURL import SpliceURL
from model.Practicalusing.counterlist import CounterList
from model.advertising.tmpSolvePerson import TmpSolvePerson
from model.advertising.Returnvaluedefine import ReturnValuedefine
  
def cminitdata():
    
    # url unified 
    geturlunified = initcheck(UnifiedURL)
    if int(geturlunified) == 0:
        CMDBSession.add(UnifiedURL('reg.ztgame.com','快速注册校验url','testreg',1))
    
    # dnsip unified
    getdnsipunified = initcheck(UnifiedDNSIP)
    if int(getdnsipunified) == 0:
        CMDBSession.add(UnifiedDNSIP('101.226.182.18',1))
        CMDBSession.add(UnifiedDNSIP('222.73.225.205',1))
        
    # url relation with dnsip
    getrelationorurlanddns = initcheck(URLtoDNS)
    if int(getrelationorurlanddns) == 0:
        CMDBSession.add(URLtoDNS(1,1))
        CMDBSession.add(URLtoDNS(1,2))
        
    # return value define
    getreturnvalueofdefine = initcheck(ReturnValuedefine)
    if int(getreturnvalueofdefine) == 0:
        CMDBSession.add(ReturnValuedefine(101,'请您输入通行证名称','testreg',1))
        CMDBSession.add(ReturnValuedefine(102,'通行证名称长度应为6-47个字符','testreg',1))
        CMDBSession.add(ReturnValuedefine(103,'通行证名称必须以字母开头','testreg',1))
        CMDBSession.add(ReturnValuedefine(104,'该通行证名称已经存在','testreg',1))
        CMDBSession.add(ReturnValuedefine(105,'通行证名称中含有不能使用的的单词:','testreg',1))
        CMDBSession.add(ReturnValuedefine(106,'通行证由数字,字母或下划线组成,并只能以字母开头,字母和数字结尾','testreg',1))
        CMDBSession.add(ReturnValuedefine(107,'单位时间内注册账号数过多','testreg',1))
        CMDBSession.add(ReturnValuedefine(201,'请您输入密码','testreg',1))
        CMDBSession.add(ReturnValuedefine(202,'密码长度应为6-16个字符','testreg',1))
        CMDBSession.add(ReturnValuedefine(203,'密码不能和通行证名称相同','testreg',1))
        CMDBSession.add(ReturnValuedefine(204,'密码必须由字母数字下划线组成','testreg',1))
        CMDBSession.add(ReturnValuedefine(205,'2次输入的密码不一致','testreg',1))
        CMDBSession.add(ReturnValuedefine(206,'重复密码不能为空','testreg',1))
        CMDBSession.add(ReturnValuedefine(301,'请输入真实姓名','testreg',1))
        CMDBSession.add(ReturnValuedefine(302,'姓名只允许为中文,例如:张三','testreg',1))
        CMDBSession.add(ReturnValuedefine(303,'姓名字数不能超过10个字符','testreg',1))
        CMDBSession.add(ReturnValuedefine(401,'请输入身份证号码','testreg',1))
        CMDBSession.add(ReturnValuedefine(402,'身份证格式错误,例如:320102198205201439','testreg',1))
        CMDBSession.add(ReturnValuedefine(403,'禁止18周岁以下未成年人注册本游戏','testreg',1))
        CMDBSession.add(ReturnValuedefine(501,'请输入验证码','testreg',1))
        CMDBSession.add(ReturnValuedefine(502,'验证码失效','testreg',1))
        CMDBSession.add(ReturnValuedefine(503,'验证码错误','testreg',1))
        CMDBSession.add(ReturnValuedefine(601,'请确认您已阅读并同意《巨人用户协议》','testreg',1))
        CMDBSession.add(ReturnValuedefine(701,'系统错误,请稍候再试','testreg',1))
        
    # splice url 
    getspliceurlof = initcheck(SpliceURL)
    if int(getspliceurlof) == 0:
        CMDBSession.add(SpliceURL('testreg','http://(%s)/registe/fastReg?check=form&username=(%s)&userpwd=123456&realname=%E5%BC%A0%E4%B8%89&idnum=362502198611185412&hasValidateCode=1&source=xxsj_mobile_app&mobile_app=xxsj_mobile_app',0))
        
    # counter list
    getcounterlist = initcheck(CounterList)
    if int(getcounterlist) == 0:
        CMDBSession.add(CounterList('101.226.182.55'))
        CMDBSession.add(CounterList('222.73.243.210'))
        CMDBSession.add(CounterList('101.226.182.61'))
        CMDBSession.add(CounterList('101.226.182.54'))
        
    gettmpsolveuser = initcheck(TmpSolvePerson)
    if int(gettmpsolveuser) == 0:
        CMDBSession.add(TmpSolvePerson('侯心刚',13817234504))
        
    CMDBSession.commit()
        
# used to check instance count
def initcheck(Tableinstance):
    
    getfromSearch = CMDBSession.query(Tableinstance).all()
    
    return len(getfromSearch)
