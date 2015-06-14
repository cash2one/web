# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from model.dbsearch import AlarmSearch, EventTransportSearch, EventTransportExpand
from BaseClass.verifityDependence import changeDict, base64Data
from BaseClass.timeBasic import TimeBasic

class ExpandStep:
    
    def __init__(self):
        
        self.returns = ""
        
    def compareUser(self, userDict, username):
        
        ''' Part Control : operation = 0 '''
        for eachUserID, eachUserStatus in userDict.items():
            getResultofalarmsearch = AlarmSearch().SureUserInformation(eachUserID)
            if getResultofalarmsearch['Status'] == 'Success':
                if getResultofalarmsearch['userName'] == username:
                    return dict(Status='Success', operation=0)
        
        ''' Part See : operation = 1 '''        
        getSearchofotherpart = AlarmSearch().Broadcast(-1)
        if getSearchofotherpart['Status'] != 'Success':
            return dict(Status='False', JsonChar=getSearchofotherpart['msg'])

        else:
            tmplist = []
            for eachlistofGroup in getSearchofotherpart['BroadCastList']:
                getUserIDforAll = AlarmSearch().getRelationofUser(eachlistofGroup)
                if getUserIDforAll['Status'] == 'Success':
                    del getUserIDforAll['Status']
                    for key,value in getUserIDforAll.items():
                        tmplist.append(key)
                            
            tmplist={}.fromkeys(tmplist).keys()
            
            for eachuser in tmplist:
                gettmpcompare = self.compareEachUser(eachuser, username)
                if gettmpcompare['Status'] == 'Success':
                    return dict(Status='Success', operation=1)
            
        ''' Part title : operation = 2 '''
        getSearchofuserExistSingle = EventTransportSearch().searchUserExist(username)
        if getSearchofuserExistSingle['Status'] != 'Success':
            return getSearchofuserExistSingle
        else:
            return dict(Status='Success', operation=2)
        
        return dict(Status='False', msg='This user is not Allowed to select in Page.')
            
    def compareEachUser(self, eachuser, username):
        
        getResultofalarmsearch = AlarmSearch().SureUserInformation(eachuser)
        if getResultofalarmsearch['Status'] == 'Success':
            if getResultofalarmsearch['userName'] == username:
                return dict(Status='Success')
                
        return dict(Status='False')
    
    
    def explainData(self, data):
        
        if type(data).__name__ == 'str':
            newData = base64Data().decode64(data)
            if re.search(r'{|}',newData):
                newData = eval(newData)
            else:
                newData = newData
        else:
            newData = data
            
        return newData
    
    def explainTimestamp(self, timestamp):
        
        newTime = TimeBasic().timeControl(timestamp, 3)
        
        return newTime
    
    def searchfromeventdoing(self, GameID, EventGrade):
        
        # GameID
        if GameID != 'None' and type(EventGrade).__name__ == 'NoneType':
            getResult = EventTransportExpand().searcheventdoingbyGameID(GameID)
            if getResult['Status'] != 'Success':
                return getResult
            else:
                return getResult
        elif GameID != 'None' and EventGrade == 'None':
            getResult = EventTransportExpand().searcheventdoingbyGameID(GameID)
            if getResult['Status'] != 'Success':
                return getResult
            else:
                return getResult
        # EventGrade   
        elif type(GameID).__name__ == 'NoneType' and  EventGrade != 'None':
            getGradeResult = EventTransportExpand().searchdetailbygrade(EventGrade)
            if getGradeResult['Status'] != 'Success':
                return getGradeResult
            else:
                return getGradeResult
        elif GameID == 'None' and EventGrade != 'None':
            getGradeResult = EventTransportExpand().searchdetailbygrade(EventGrade)
            if getGradeResult['Status'] != 'Success':
                return getGradeResult
            else:
                return getGradeResult
        # GameID + EventGrade
        elif GameID != 'None' and EventGrade != 'None':
            getBothResult = EventTransportExpand().searchdetailbygameidandgrade(GameID, EventGrade)
            if getBothResult['Status'] != 'Success':
                return getBothResult
            else:
                return getBothResult
            
        