# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from Steps import BasicStep
from BroadcastManager import Manager 
from alarm.alarmScheduler import Scheduler
from BaseClass.verifityDependence import changeDict

class AlarmMain:
    
    def __init__(self):
        
        self.userDict = {}
        self.returns = ""
        
    def alarmManager(self, message):
        
        ''' 
        No.1 judge 4 Variable
        No.2 get default variable 
        No.3 analyst alarm object
        No.4 decide alarm method
        No.5 alarming
        No.6 add into table and into log
        '''

        print "### message", message
        # Step 1.
        getStepOne = BasicStep().judgeVariable(message)
        if getStepOne['Status'] != 'Success':
            return getStepOne 
        
        # Step 2. -> newmessage :  getStepTwo['message']
        getStepTwo = BasicStep().basicFilling(message)
        if getStepTwo['Status'] != 'Success':
            return getStepTwo

        # Step 3.
        # A. get GameID by GameName
        getGameID = Scheduler().getGameIDbygameName(getStepTwo['message']['Project'])
        print "### getGameID:", getGameID
        # B. get eventgroup by gameName
        EventGroup = Scheduler().getEventGroupRelation(getStepTwo['message']['Project'])
        print "### EventGroup:", EventGroup
        if EventGroup['Status'] != 'Success':
            return EventGroup
        # C. get Prople list -> self.userDict
        for eachGroup in EventGroup['grouplist']:
            tmppeople = Scheduler().getPeople(int(getStepTwo['message']['Eventlevel']), eachGroup)
            if len(tmppeople) == 0:
                self.userDict = self.userDict
            else:
                if tmppeople['Status'] == 'Success':
                    self.userDict = dict(self.userDict, **tmppeople)
       
        if self.userDict['Status']:
            del self.userDict['Status']
              
        print "####### userDict:", self.userDict      
        # step 4. 
        ''' 
        This method used by check alarm method 
        if oc = 0 : means oc needn't alarm
        if oc = 1 : means oc need alarm
        if mail = 0: means mail needn't alarm
        if mail = 1: means mail need alarm
        if smcd = 0: means smcd needn't alarm
        if smcd = 1: means smcdneed alarm
        '''
        getdecidemethod = BasicStep().decideEvent(int(getStepTwo['message']['Eventlevel']), getStepTwo['message']['Mbody']) 
        if getdecidemethod['Status'] != 'Success':
            return getdecidemethod

        # step 5.    This part is block, after broadcast to everybody in group
        #            Then will be return {'Status': 'Success'} 
        getBroadreturn = Manager().Main(self.userDict, getStepTwo['message']['Mbody'])
        if getBroadreturn['Status'] != 'Success':
            return getBroadreturn
        
        # step 6. into event recode table
        getrecode = Scheduler().eventintoTable(getGameID['GameID'], int(getStepTwo['message']['Eventlevel']), getStepTwo['message']['Mbody'], getStepTwo['message']['Timestamp'], 0)
        if type(getrecode).__name__ != 'dict':
            return dict(Status='Success', msg='Same Data Input and be rollbacked.')
        
        return dict(Status='Success')
            
    def alarmManagerTest(self, message):
        
        ''' 
        No.1 judge 4 Variable
        No.2 get default variable 
        No.3 analyst alarm object
        No.4 decide alarm method
        No.5 print into log
        '''
        
        # Step 1.
        getStepOne = BasicStep().judgeVariable(message)
        if getStepOne['Status'] != 'Success':
            return getStepOne 
        
        # Step 2. -> newmessage :  getStepTwo['message']
        getStepTwo = BasicStep().basicFilling(message)
        if getStepTwo['Status'] != 'Success':
            return getStepTwo

        # Step 3.
        # A. get GameID by GameName
        getGameID = Scheduler().getGameIDbygameName(getStepTwo['message']['Project'])
        # B. get eventgroup by gameName
        EventGroup = Scheduler().getEventGroupRelation(getStepTwo['message']['Project'])
        # C. get Prople list -> self.userDict
        for eachGroup in EventGroup:
            tmppeople = Scheduler().getPeople(int(getStepTwo['message']['Eventlevel']), eachGroup)
            if len(tmppeople) == 0:
                self.userDict = self.userDict
            else:
                if tmppeople['Status'] == 'Success':
                    self.userDict = dict(self.userDict, **tmppeople)
       
        if self.userDict['Status']:
            del self.userDict['Status']
              
        # step 4. 
        getdecidemethod = BasicStep().decideEvent(int(getStepTwo['message']['Eventlevel']), getStepTwo['message']['Mbody']) 
        if getdecidemethod['Status'] != 'Success':
            return getdecidemethod

        # step 5.    This part is block and print in the STDOUT
        getBroadreturn = Manager().TestBroadcastMain(self.userDict, getStepTwo['message']['Mbody'])
        if getBroadreturn['Status'] != 'Success':
            return getBroadreturn
        
        return dict(Status='Success')       
    
    def alarmManagerbyoid(self, message):
        
        ''' 
        No.1 judge 4 Variable
        No.2 get default variable 
        No.3 analyst alarm object
        No.4 decide alarm method
        No.5 alarming
        No.6 add into table and into log
        '''

        print "### message", message
        # Step 1.
        getStepOne = BasicStep().judgeVariablebyoid(message)
        if getStepOne['Status'] != 'Success':
            return getStepOne 
        
        # Step 2. -> newmessage :  getStepTwo['message']
        getStepTwo = BasicStep().basicFillingbyoid(message)
        if getStepTwo['Status'] != 'Success':
            return getStepTwo

        # Step 3.
        # A. get GameID by GameName
        getGameID = Scheduler().getGameIDbygameName(getStepTwo['message']['Project'])
        print "### getGameID:", getGameID
        # B. get eventgroup by gameName
        EventGroup = Scheduler().getEventGroupRelation(getStepTwo['message']['Project'])
        print "### EventGroup:", EventGroup
        if EventGroup['Status'] != 'Success':
            return EventGroup
        # C. get Prople list -> self.userDict
        for eachGroup in EventGroup['grouplist']:
            tmppeople = Scheduler().getPeople(int(getStepTwo['message']['Eventlevel']), eachGroup)
            if len(tmppeople) == 0:
                self.userDict = self.userDict
            else:
                if tmppeople['Status'] == 'Success':
                    self.userDict = dict(self.userDict, **tmppeople)
       
        if self.userDict['Status']:
            del self.userDict['Status']
              
        print "####### userDict:", self.userDict      
        # step 4. 
        ''' 
        This method used by check alarm method 
        if oc = 0 : means oc needn't alarm
        if oc = 1 : means oc need alarm
        if mail = 0: means mail needn't alarm
        if mail = 1: means mail need alarm
        if smcd = 0: means smcd needn't alarm
        if smcd = 1: means smcdneed alarm
        '''
        getdecidemethod = BasicStep().decideEvent(int(getStepTwo['message']['Eventlevel']), getStepTwo['message']['Mbody']) 
        if getdecidemethod['Status'] != 'Success':
            return getdecidemethod

        # step 5.    This part is block, after broadcast to everybody in group
        #            Then will be return {'Status': 'Success'} 
        getBroadreturn = Manager().Main(self.userDict, getStepTwo['message']['Mbody'])
        if getBroadreturn['Status'] != 'Success':
            return getBroadreturn
        
        # step 6. into event recode table
        getrecode = Scheduler().eventintoTable(getGameID['GameID'], int(getStepTwo['message']['Eventlevel']), getStepTwo['message']['Mbody'], getStepTwo['message']['Timestamp'], 'None', 0, 0, 0, getStepTwo['message']['Oid'])
        if type(getrecode).__name__ != 'dict':
            return dict(Status='Success', msg='Same Data Input and be rollbacked.')
        
        return dict(Status='Success')