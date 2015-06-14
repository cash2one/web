# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys
import time

from suds import WebFault
from suds.client import Client
import simplejson as json

from ServiceConfig.config import readFromConfigFile
from BaseClass.verifityDependence import changeDict

class LoginAuthorized:
    
    def __init__(self):
        
        self.url = ""
        self.username = ""
        self.passwd = ""
        self.loginType = ""
        self.nowTime = ""
        self.readDict = {}
        
        # to get the windowsAD url path
        getConfigAnalyst = readFromConfigFile().get_config_sqlalchemy('/WebserviceInterface/ServiceConfig/setting.ini')

        self.url = getConfigAnalyst['windowsAD'][0][1]


    def ADLogin(self, getCharacter):
        
        # explain getCharacter to Dict
        jsonDict = changeDict().strtodict(getCharacter)  
        
        for key,value in jsonDict.items():
            if key == 'loginUserName':
                self.username = value
            elif key == 'loginPassword':
                self.passwd = value
        
        self.nowTime = int(time.time())
        
        # windows AD authorized
        client = Client(self.url)
        
        getADreturn = client.service.ValidateAdOnlyByPasswd(self.username,self.passwd)
        getAttritude = getADreturn["return_flag"]
        
        return dict(Status=getAttritude, Username=self.username, Password=self.passwd, validateTime=self.nowTime)

    def getUserInformation(self, Username):
        
        client = Client(self.url)
        
        getInformation = client.service.QueryAdUserInfoByName(Username)
        
        user_name = getInformation['user_name']
        mail = getInformation['mail']
        staffnum = getInformation['staffnum']
        telephone = getInformation['telephonenumber']
        
        return dict(Username=user_name, Mail=mail, Staffnum=staffnum, Telephone=telephone)

        # 获取所有信息
        #print client
        # 获取用户验证信息： 成功： 登录成功    失败：密码错误  boolean
        #print client.service.ValidateAdOnlyByPasswd('majian','ztgame@678')
        # 获取用户的验证信息并附加token
        #print client.service.ValidateAdByPasswd('majian','ztgame@678','192.168.82.89','192.168.82.89')
        # 获取用户基本信息
        #print client.service.QueryAdUserInfoByName(self.username)
