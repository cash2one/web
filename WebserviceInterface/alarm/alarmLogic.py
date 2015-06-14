# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from model.dbsearch import AlarmSearch

class Logic:
    
    def __init__(self):
        
        self.returns = ""
        self.userlist = []
        self.userdict = {}
        
    ''' choose user to be broadcast by eventgrade '''    
    def SieveUser(self, groupDict, eventGrade):
        
        for uid,ulevel in groupDict.items():
            if int(ulevel) >= int(eventGrade):
                self.userlist.append(uid)
                
        return self.userlist
    
    ''' 
    get User inform about user 
    example : {'majian': {'MAIL': 'majian@ztgame.com', 'OC': 'majian@ztgame.com', 'SMCD': '13817992612'} }
    '''
    def UserInformGet(self, userlist):
        
        for eachUser in userlist:
            getEach = AlarmSearch().SureUserInformation(eachUser)
            if getEach['Status'] == 'Success':
                self.userdict['Status'] = 'Success'
                self.userdict[getEach['userName']] = dict(OC=getEach['OC'], SMCD=getEach['SMCD'], MAIL=getEach['MAIL'])
                
        return self.userdict
    
    ''' 
    part use to get monitor time 
    example :  This Zone 5 mins Lose -2000 people.
    '''
    def getMonitorTime(self, data):
        
        RebackDict = {}
        
        print "#### data", data
        
        if re.search(r'no changes', data):
            RebackDict['Status'] = 'Success'
            RebackDict['time'] = re.split('\s+', data)[2]
            RebackDict['people'] = 0
        else:
            RebackDict['Status'] = 'Success'
            RebackDict['time'] = re.split('\s+', data)[2]
            tmpPeople = re.split('\s+', data)[5]
            if int(tmpPeople) < 0:
                RebackDict['people'] = abs(int(tmpPeople))
            else:
                RebackDict['people'] = 0
            
        return RebackDict
    
    ''' get Data be part by | and return list '''
    def getDataList(self, data):
        
        newList = []
        tmpList = []
        tmpList = re.split('\|', data)
        
        for eachlist in tmpList:
            changeOk = self.changeSTRtoDict(eachlist)
            newList.append(changeOk)
        
        return newList
    
    ''' get STRING to Dict '''
    def changeSTRtoDict(self, stringChar):

        if type(stringChar).__name__ == 'str' and stringChar != '':
        
            reStr = eval(stringChar)
        
            return reStr
        
        else:
            return ''