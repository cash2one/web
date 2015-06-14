# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
from EventScheduler import MainScheduler, AlarmScheduler, ExplainScheduler
from BaseClass.stack import Stack
from event.Base.eventCalc import EventCalc
from eventdefine import EventDefine

class Eventcontroller:
    
    def __init__(self):
        
        self.count = 0
        self.scheduler = ""
        self.newStack = ""
        
    def MainScheduler(self, body):
        
        ''' No.1 Control Body has Eight Variables '''
        getBodycheck = self.FirstCheckBody(body)
        if getBodycheck != 'Success':
            return getBodycheck
        
        ''' No.2 check body's OID '''
        getOIDcheck = MainScheduler().searchOID(body['OID'])
        if getOIDcheck['Status'] != 'Success':
            return getOIDcheck['msg']

        ''' No.3 create a new stack -> Usage : to Store temp defined message '''
        self.newStack = Stack()
        self.newStack.push(body)
        
        ''' --------- No.4 Event Analyst ### Loop through the stack ---------- '''
        while self.newStack.isEmpty() == False:
            
            # {'Status': 'Success', 'Info': '', 'OID': '1.1.2.2.3.3.4.6', 'JobID': '0', 'Result': "{u'memory': 75}", 'Type': 'agent', 'ID': '1', SendTime=1368484474}
            # {'Result': "{u'ZTQY': u'Could not found ONLINENUM20130306', u'SGZH': {u'11111': [22222, 22222, 23222], u'22222': [11111, 11111, 12111]}}"}
            tmpPartAnalystbody = self.newStack.pop()
            
            # {'Status': 'Success', 'eventType': 0L, 'eventVar': 'disk,memory'}
            # {'Status': 'Success', 'eventType': 1L, 'eventVar': ''}
            getOIDdetail = MainScheduler().searchOIDdetail(tmpPartAnalystbody['OID'])
            if getOIDdetail['Status'] == 'False':
                return getOIDdetail['msg']
            
            # {'Status': 'Success', 'TemplateType': 'numberofcurves', 'oid': '1.1.6.0.0.1.2.34.21'}
            getOIDname = MainScheduler().searchOIDname(tmpPartAnalystbody['OID'])
            if getOIDname['Status'] == 'False':
                return getOIDname
            
            ''' 
            get simple or complex event
            example : {'Status': 'Success', 'hold':'ThresHold'}
                    : {'Status': 'Success', 'hold':'ComplexHold'}
            '''
            geteventType = MainScheduler().readconfig_tableRelation(getOIDdetail['eventType'])
            if geteventType['Status'] == 'False':
                return geteventType['msg']
            
            #''' ThresHold '''                                                                                                                                                                                                                                                                                                                                                                                    
            if getOIDdetail['eventVar'] != '':
                tmpList = []
                tmpList = re.split(r',', getOIDdetail['eventVar'])
            
                for eachVar in tmpList:
                    ''' 
                    get judge from each Var thres
                    example : {'Status': 'Success', 'Return':"String,60%,80%,0'}
                    '''
                    geteventVar = MainScheduler().readconfig_ThresHold(eachVar)
                    if geteventVar['Status'] == 'Success':
                        tryList = re.split(r',', geteventVar['Return'])
                        ''' 
                        get judge from config calculation  
                        example : {'Status': 'Success', 'Return': 'noneed'}
                        '''
                        getCALC = MainScheduler().readconfig_thresCalculation(tryList[-1])
                    
                        '''  using whole Dispatch '''
                        allResult = MainScheduler().getAllscheduler(tmpPartAnalystbody['OID'], eachVar, geteventVar['Return'], tmpPartAnalystbody['Result'], getCALC['Return'])
                        if not allResult:
                            return 'False'
                    
                        ''' Throught into Alarm'''
                        # choose a method to alarm
                    
                        getReturn = AlarmScheduler().AlarmControl(tmpPartAnalystbody['OID'])
            
            #''' ComplexHold '''            
            elif getOIDdetail['eventVar'] == '':
                ''' 
                No.1 This Method of OID calcuation : templatetype used to judge method 
                {u'ZTQY': u'Could not found ONLINENUM20130306', 
                 u'SGZH': {
                            u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [{'Allcount': 27222}, {'Losecount': 0}, {'Percent': '0%'}], 
                            u'\u53cc\u7ebf2\u533a': [{'Allcount': 11111}, {'Losecount': -2000}, {'Percent': '18%'}]
                          }
                }
                ''' 
                eventcount = EventCalc().CalcControl(getOIDname['TemplateType'], tmpPartAnalystbody['Result'])
                print "##### No.1 This Method of OID calcuation:", eventcount
                
                ''' 
                No.2 event defined : PASS : use zhangminjie singal && 基本阀值判断带templatetype参数 
                {u'ZTQY': u'Could not found ONLINENUM20130306', 
                 u'SGZH': {
                           u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [{'LosePeople': 'NotOver'}, {'LosePercent': 'NotOver'}], 
                           u'\u53cc\u7ebf2\u533a': [{'LosePeople': 'NotOver'}, {'LosePercent': 'Over'}]
                          }
                }
                '''
                getDefine = EventDefine().defineManager(getOIDname['TemplateType'], tmpPartAnalystbody['SendTime'], eventcount)
                print "##### No.2 event defined :",getDefine
                
                ''' No.3 event relation : PASS'''
                print "##### No.3 event relation : PASS"
                
                ''' No.4 event level count : PASS : default 4 '''
                print "##### No.4 event level count : PASS"

                ''' No.5 event upgrade : PASS : default no '''
                print "##### No.5 event upgrade : PASS"
                
                ''' 
                No.6 event explain to Human 
		Situation 1. {'ZTII': {'ReturnValue': {'percent': {'Status': 'Over', 'hold': '2', 'actual': 3}}}}

		Situation 2. 
                {u'ZTQY': u'can not get number of curves from platform , perhaps ONLINENUM20130306 not exist.', 
                 u'SGZH': {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [{'TimeOccur': '2013\xe5\xb9\xb403\xe6\x9c\x8821\xe6\x97\xa5_14:54\xe5\x88\x86', {'Actual': 13000, 'LosePeople': 'Over', 'Standard': 10000}, {'LosePercent': 'Over', 'Actual': '54%', 'Standard': '10%'}],
                           u'\u53cc\u7ebf2\u533a': [{'TimeOccur': '2013\xe5\xb9\xb403\xe6\x9c\x8821\xe6\x97\xa5_14:54\xe5\x88\x86', {'LosePercent': 'Over', 'Actual': '18%', 'Standard': '10%'}]
                          }
                }
                '''
                getExplain = ExplainScheduler().ExplaintoHuman(getOIDname['TemplateType'], getDefine)
                print "##### No.6 event explain :", getExplain
                
                ''' No.7 insert into database and keep in Track '''
                getAdd = MainScheduler().addIntoAlarm(False, 4, tmpPartAnalystbody['OID'], getExplain)
                print "##### No.7 insert into database:", getAdd
                
                ''' No.8 Alarm to platform : for different to push '''
                getReturn = AlarmScheduler().AlarmControl(tmpPartAnalystbody['OID'])
                
                ''' No.9 '''
                
                
        return "Success"
    
    
    def FirstCheckBody(self, body):
        
        for key,value in body.items():
            if key == 'Status':
                self.count += 1
            elif key == 'Type':
                self.count += 1
            elif key == 'Result':
                self.count += 1
            elif key == 'Info':
                self.count += 1
            elif key == 'ID':
                self.count += 1
            elif key == 'OID':
                self.count += 1
            elif key == 'JobID':
                self.count += 1
            elif key == 'SendTime':
                self.count += 1
        
        if self.count == 8:
            return "Success"
        else:
            return "False"
