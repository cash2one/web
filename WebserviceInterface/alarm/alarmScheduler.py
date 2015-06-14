# -*- coding: utf-8 -*-
''' @author : majian'''

import time
import os, re, sys

from alarmLogic import Logic
from BaseClass.readCurves import ReadCurves
from model.dbsearch import LogicSearch, DataSearch, TranslateSearch, EventSearch, AlarmSearch, CircultSearch
from model.eventAlarm import EventAlarm
from interface.lync import Alarm
from interface.mail import SendMail
from interface.smcd import SMCDinterface

class Scheduler:
    
    def __init__(self):
        
        self.returns = ""
        self.grouplist = []
        self.userinformation = {}
        
    ''' 
    Get the information in database table.eventalarm 
    OID = input && status = 'Inuse'
    '''    
    def getSearchofAlarm(self, OID):
        
        getSearchResult = AlarmSearch().searchinAlarm(OID)
        
        return getSearchResult
    
    def readlisttoMan(self, list):
        
        getlistResult = ReadCurves().changeReadlist(list)
        
        return getlistResult
    
    def AlarmByOC(self, fromUser, toUser, data):
        
        print "######### data", data
        
        Alarm().officeCommunicate(fromUser, toUser, data)
        
        return True
    
    def AlarmByMail(self, fromUser, toUser, sub, content):
        
        SendMail().send_mail(fromUser, toUser, sub, content)
        
        return True
    
    def AlarmBySMCD(self, dest_mobile, msg_content, sender):
        
        SMCDinterface().sendingMessage(dest_mobile, msg_content, sender)
        
        return True
    
    ''' throught gameName to get groupName, userName and other information '''
    def getEventGroupRelation(self, gameName):
        
        ''' 
        No.1 get gameID 
        example : {'Status': 'Success', 'GameID': 32L} 
        '''
        getReturnStatus = AlarmSearch().sureGameStatus(gameName)
        if getReturnStatus['Status'] != 'Success':
            return getReturnStatus
        
        ''' 
        No.2 get groupID
        example : {'Status': 'Success', 'groupID': 0L}
        '''
        getReturnRelation = AlarmSearch().sureProjectGroup(getReturnStatus['GameID'])
        if getReturnRelation['Status'] != 'Success':
            return getReturnRelation
        
        ''' 
        No.3 sure group exist and add into self.grouplist
        example : {'Status': 'Success'}
        '''
        getSureGroup = AlarmSearch().sureGroupExist(getReturnRelation['groupID'])
        if getSureGroup['Status'] != 'Success':
            return getSureGroup
        
        self.grouplist.append(getReturnRelation['groupID'])
        
        '''
        No.4 add All group which will'b broadcast
        '''
        getBroadcast = AlarmSearch().Broadcast()
        if getBroadcast['Status'] != 'Success':
            return getBroadcast
        
        self.grouplist = list(set(self.grouplist) | set(getBroadcast['BroadCastList']))
        
        return dict(Status='Success',grouplist=self.grouplist)

    ''' Depend eventgrade and groupID to get people list '''
    def getPeople(self, eventGrade, groupID):
        
        ''' No.1 get User '''
        getUser = AlarmSearch().getRelationofUser(groupID)
        if getUser['Status'] != 'Success':
            return getUser
        
        del getUser['Status']
        
        ''' No.2 Judge User level '''
        getUserlevel = Logic().SieveUser(getUser, eventGrade)
        
        ''' No.3 get User information '''
        self.userinformation = Logic().UserInformGet(getUserlevel)
        
        return self.userinformation
    
    ''' Depend GameSimple to get GameChineseName '''
    def getGameNameCH(self, gameName):
        
        getFullname = AlarmSearch().getgameNameCH(gameName)
        
        return getFullname
    
    ''' Throught this Method to analyst data '''
    def getTimeandPeople(self, data):
        
        getReturns = Logic().getMonitorTime(data)
        
        return getReturns
    
    ''' Data be part '''
    def dataListpart(self, data):
        
        getDataPart = Logic().getDataList(data)
        
        return getDataPart
    
    ''' get GameID by gameName '''
    def getGameIDbygameName(self, gameName):
        
        getGameID = AlarmSearch().sureGameStatus(gameName)
        
        return getGameID
    
    ''' get eventgrade by gameeventgrade detail '''
    def geteventgraderelation(self, eventgrade):
        
        getgrade = AlarmSearch().geteventgraderelation(eventgrade)
        
        return getgrade
    
    ''' insert into table about event '''
    def eventintoTable(self, gameID, eventGrade, data, timestamp, TakeoverPerson='None', Status=0, SustainableTime=0, carepeoplecount=0, Oid=0):
        
        getcircultSearch = CircultSearch().addCircult(gameID, eventGrade, data, timestamp, TakeoverPerson, Status, SustainableTime, carepeoplecount, Oid)
        
        return getcircultSearch
        