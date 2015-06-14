# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys

from suds import WebFault
from suds.client import Client
import simplejson as json

from ServiceConfig.config import readFromConfigFile
from BaseClass.verifityDependence import changeDict

class Alarm:
    
    def __init__(self):
        
        self.url = ""
        self.passInform = ""
        
        getConfigAnalyst = readFromConfigFile().get_config_lync('/WebserviceInterface/ServiceConfig/setting.ini')
        
        self.url = getConfigAnalyst['Lync'][0][1]
        

    def officeCommunicate(self, fromUser='None', toUser='None', data='None', redirect='None'):
        
        client = Client(self.url)
        
        SureFromUser = self.sureUser(fromUser)
        if SureFromUser['Status'] == 'Success':
            fromUser = SureFromUser['UserName']
        else:
            return SureFromUser['msg']
        
        SureToUser = self.sureUser(toUser)
        if SureToUser['Status'] == 'Success':
            toUser = SureToUser['UserName']
        else:
            return SureToUser['msg']
        
        SureRedirectUrl = self.sureHttp(redirect)
        if SureRedirectUrl['Status'] == 'Success':
            redirect = SureRedirectUrl['redirect']
        else:
            return SureRedirectUrl['msg']
        
        client.service.PushUserNotification(fromUser, toUser, data, redirect)
        
        return dict(Status='Success')
        
    def sureUser(self, UserName):
        
        if re.search(r'ztgame.com', UserName):
            return dict(Status='Success', UserName=UserName)
        else:
            return dict(Status='False', msg='UserName : %s ERROR.' % UserName)
        
    def sureHttp(self, redirectUrl):
            
        if re.search(r'http\://', redirectUrl) or redirectUrl == 'None':
            return dict(Status='Success', redirect=redirectUrl)
        else:
            return dict(Status='False', msg='Redirect Url is not Right.')
