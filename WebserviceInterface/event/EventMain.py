# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from BaseClass.verifityDependence import changeDict
from ServiceConfig.config import readFromConfigFile
from model.dbsearch import AlarmSearch, EventTransportSearch, CircultSearch, EventTransportExpand 

from Depend import Dependence
from EventScheduler import Oidscheduler
from EventManager import Manager
from eventStep import EventProcessStep
from EventLevel import Eventlevel
from event.Base.bodystruct import EventBody, AlarmBody
from event.EventContent import eventContent
from interface.collection.dbconnect import Connect
from oidDecide import OidDecide

from alarm.Main import AlarmMain

class EventMain:
    
    def __init__(self):
        
        self.tablename = ""
        self.columname = ""
        self.mainserver = {}
        self.Return = {}
        self.linkwithdatabase = {}
    
    ''' 30000 message use method '''
    def CaptureMessage(self, message):
        
        ExceptionDict = {}
        
        ''' Step 1. judge message has 8 Variable '''
        getCheckbody = Dependence().CheckBody(message)
        if getCheckbody['Status'] != 'Success':
            return getCheckbody
        
        ''' Step 2. judge message data '''
        getcheckData = Dependence().checkBodydata(message)
        if getcheckData['Status'] != 'Success':
            return getcheckData
        
        message = getcheckData['message']
       
        ''' Step 3. part Of Oid to decide which to choose. '''
        getRebackofoid = OidDecide().OidCharge(message['OID'], message)
        if getRebackofoid['Status'] != 'Success':
            getRebackofoid = dict(getRebackofoid, **dict(Oid=message['OID'], Type=message['Type'], ID=message['ID']))
            
        return getRebackofoid
   
        
#        ''' 
#        Step 3. check OID and get OID name 
#         {'Status': 'Success', 'TemplateType': 'processInform'}
#        '''
#        getOidtype = Oidscheduler().getOidtypebyOID(message['OID'])
#        if getOidtype['Status'] != 'Success':
#            return getOidtype
#        
#        '''
#        Step 4. insert into temp table tempprocess
#        '''
#        getSearchMain = Manager().ManagerDecide(message, getOidtype['TemplateType'])
#        if getSearchMain['Status'] != 'Success':
#            return getSearchMain
#        
#        '''
#        Step 5. judge event 
#        example : {'Status': 'False', 'content': ['CharServer14']}
#                  {'Status': 'Success'}
#        '''
#        getStepReturn = EventProcessStep().processStep(getOidtype['TemplateType'], getSearchMain['Return']['Hostname'], message['SendTime'])
#        if getStepReturn['Status'] != 'Success':
#            return getStepReturn
#        
#        ''' 6 change content
#        example : {'content': 'ZR-Agent-4.x-test \xe7\xbc\xba\xe5\xb0\x91\xe5\xa6\x82\xe4\xb8\x8b\xe8\xbf\x9b\xe7\xa8\x8b: CharServer14', 'Status': 'Success'}
#        '''
#        getContent = eventContent().changeContent(getOidtype['TemplateType'], getSearchMain['Return']['Hostname'], getStepReturn['content'])
#        if getContent['Status'] != 'Success':
#            return getContent
#        
#        ''' 7. event update '''
#        
#        '''
#        Step 8. event level calc : not write
#        '''
#        getlevelreturn = Eventlevel().eventleveldefine(getOidtype['TemplateType'], getStepReturn['content'])
#        if getlevelreturn['Status'] != 'Success':
#            return getlevelreturn
#        
#        '''
#        Step 9. get basic information 
#                A. judge >>> localhost <<< -> >>> localhost_ipaddress <<<
#                B. get GameID
#                C. change data struct
#        '''
#        # A. {'Status': 'Success', 'hostname': 'ZR-Agent-4.x-test', 'ipaddress': '192.168.1.1'}
#        #    {'Status': 'False', 'msg':''}
#        JudgeHostname = EventProcessStep().HostnameJudge(getOidtype['TemplateType'], getSearchMain['Return']['Hostname'], getSearchMain['Return']['Ipaddress'])
#        if JudgeHostname['Status'] != 'Success':
#            return JudgeHostname
#        
#        # B. {'Status': 'Success', 'Name': 'ZT2'}
#        #    {'Status': 'False', 'msg':''}
#        getGameName = EventProcessStep().getGameID(JudgeHostname['hostname'])
#        if getGameName['Status'] != 'Success':
#            return getGameName
#        
#        # C.
#        Eventbody = EventBody().bodystructs(getOidtype['TemplateType'], getGameName['Name'], getContent['content'], 5, message['OID'], int(message['SendTime']), 1)
#        Alarmbody = AlarmBody().bodystructs(getOidtype['TemplateType'], getGameName['Name'], 5, getContent['content'], int(message['SendTime']))
#        
#        ''' Step 10. using alarm module '''
#        getAlarm = AlarmMain().alarmManager(Alarmbody['alarmbody'])
#        
#        if getAlarm['Status'] == 'Success':
#            return getAlarm
        
        
                        
    ''' 31000 message use Method '''    
    def MainControl(self, message):
        
        ''' 
        This method used to control all main events and control it by MainServer
        '''
        
        ''' No.1 : check message input -> dict '''
        if type(message).__name__ != 'dict':
            message = changeDict().strtodict(message)
            
        ''' No.2 : check message '''
        getcheckReturn = Dependence().SearchStep(message)
        if getcheckReturn['Status'] != 'Success':
            return getcheckReturn
        
        ''' No.3 : check data '''
        getcheckData = Dependence().Checkdata(message)
        if getcheckData['Status'] != 'Success':
            return getcheckData
        
        message = getcheckData['message']
        
        for eachGameID in message['Eproject']:
            getAddintoeventresult = CircultSearch().addCircult(eachGameID, message['Elevel'], message['Econtent'], message['Etimestamp'], 'None', 0, 48, 0, message['Eoid'])
            if getAddintoeventresult['Status'] != 'Success':
                return dict(Status='False', msg=getAddintoeventresult['msg'])
        
        return dict(Status='Success', message=message)
    
    ''' 31100 message test method '''    
    def TestMainControl(self, message):
        
        ''' 
        This method used to control all main events 
        '''
        
        ''' No.1 : check message input -> dict '''
        if type(message).__name__ != 'dict':
            message = changeDict().strtodict(message)
            
        ''' No.2 : check message '''
        getcheckReturn = Dependence().SearchStep(message)
        if getcheckReturn['Status'] != 'Success':
            return getcheckReturn
        
        ''' No.3 : check data '''
        getcheckData = Dependence().Checkdata(message)
        if getcheckData['Status'] != 'Success':
            return getcheckData
        
        message = getcheckData['message']
        
        return dict(Status='Success', message=message)