# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys
from BaseClass.verifityDependence import changeDict

from EventScheduler import Oidscheduler

class OidAnalyst:
    
    def __init__(self):
        
        self.oid = ""
        self.Request = ""
        self.couldbeNull = ""
        self.timepass = ""
        self.timestamp = ""
        self.getpynames = []
        self.getResult = []
        self.returns = {}
        self.getStruct = {}
    
    ''' This method is used to check Now Curves of people '''     
    def AnalystTransportData(self, ResourceDict):
        
        ''' {'timepass': '5', 'OID': '1.1.6.0.0.1.2.34.21', 'Request': "{u'gameid': [32]}"} '''
        ''' No.1 judge OID '''
        
        for key,value in ResourceDict.items():
            if key == 'OID':
                self.oid = value
            elif key == 'Request':
                self.Request = value
            elif key == 'timePass':
                self.timepass = value
        
        if self.oid == '':
            return 'OID is None, please check input.'
        
        ''' No.2 judge body can be NULL'''
        self.couldbeNull = Oidscheduler().SearchOidNullable(self.oid)
        if len(self.Request) == 2 or len(self.Request) == 0 and self.couldbeNull == 'Success':
            ''' -> judge oid exist '''
            getItems = Oidscheduler().SearchOID(self.oid)
            if getItems['Status'] == 'Success': 
                ''' -> judge data struct '''
                self.getStruct = Oidscheduler().SearchStruct(getItems)
                
            self.returns[0]=dict(GameName=self.getStruct['gameid']['default'], timePass=self.getStruct['timepass']['default'])
            
            self.getResult.append(self.returns)
                    
            return dict(Status='Success', deAnalyst=self.getResult)
            
        elif len(self.Request) == 2 or len(self.Request) == 0 and self.couldbeNull != 'Success':
            return dict(Status='False', msg='could not support null body')
        
        elif len(self.Request) != 2 or len(self.Request) != 0:

            tmpDicts = {}
            
            ''' change Str to Dict '''
            self.Request = changeDict().strtodict(self.Request)

            for key,value in self.Request.items():
                if key == 'gameid':
                    for eachGameid in value:
                        getPYname = Oidscheduler().getPYnameaboutGameid(eachGameid)
                        if getPYname['Status'] == 'Success':
                            tmpDicts[eachGameid] = dict(GameName=getPYname['Name'], timePass=self.timepass)
                            
            self.getpynames.append(tmpDicts)
         
            return dict(Status='Success', deAnalyst=self.getpynames)      
    
    ''' This method used to judge oid of history of curves '''    
    def AnalystHistoryCurvesData(self, ResourceDict):
        
        ''' {'timestamp': '1000000000', 'OID': '1.1.6.0.0.1.2.34.22', 'Request': "{u'gameid': [32]}"} '''
        ''' No.1 judge OID '''
        
        for key,value in ResourceDict.items():
            if key == 'OID':
                self.oid = value
            elif key == 'Request':
                self.Request = value
            elif key == 'timestamp':
                self.timestamp = value
                
        if self.oid == '':
            return 'OID is None, please check input.'
        
        ''' No.2 judge body can be NULL'''
        self.couldbeNull = Oidscheduler().SearchOidNullable(self.oid)
        if len(self.Request) == 2 or len(self.Request) == 0 and self.couldbeNull == 'Success':
            ''' -> judge oid exist '''
            getItems = Oidscheduler().SearchOID(self.oid)
            if getItems['Status'] == 'Success': 
                ''' -> judge data struct '''
                self.getStruct = Oidscheduler().SearchStruct(getItems)
                
            self.returns[0]=dict(GameName=self.getStruct['gameid']['default'], timestamp=self.getStruct['timestamp']['default'])
            
            self.getResult.append(self.returns)
                    
            return dict(Status='Success', deAnalyst=self.getResult)
            
        elif len(self.Request) == 2 or len(self.Request) == 0 and self.couldbeNull != 'Success':
            return dict(Status='False', msg='could not support null body')
        
        elif len(self.Request) != 2 or len(self.Request) != 0:

            tmpDicts = {}
            
            ''' change Str to Dict '''
            self.Request = changeDict().strtodict(self.Request)

            for key,value in self.Request.items():
                if key == 'gameid':
                    for eachGameid in value:
                        getPYname = Oidscheduler().getPYnameaboutGameid(eachGameid)
                        if getPYname['Status'] == 'Success':
                            tmpDicts[eachGameid] = dict(GameName=getPYname['Name'], timestamp=self.timestamp)
                            
            self.getpynames.append(tmpDicts)
         
            return dict(Status='Success', deAnalyst=self.getpynames)                          