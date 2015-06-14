# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import simplejson as json

from BaseClass.timeBasic import TimeBasic
from eventExplain import HumanRead
from ServiceConfig.config import readFromConfigFile
from event.Base.eventAlogithm import Event
from BaseClass.verifityDependence import changeDict
from alarm.alarmControl import AlarmControl
from model.oidRelation import OidRequest, OIDVariable
from model.dbsearch import LogicSearch, DataSearch, TranslateSearch, EventSearch
from sqlalchemy.event import Events


class Oidscheduler:
    
    def __init__(self):
        
        self.returns = ""
        self.inRequest = []
        self.outRequest = []
        self.getFieldSearchResult = {}
        
    def SearchOidNullable(self, oid):
        
        ''' Sure oid could be Null '''
        getNullable = EventSearch().searchOIDexist(oid)
        if getNullable['Nullable'] == 'Y':
            return 'Success'
        else:
            return 'False'
    
    def SearchOID(self, oid):
        
        ''' Sure oid is exist or not '''
        getSearchoidResult = EventSearch().searchOIDexist(oid)

        return getSearchoidResult
    
    def SearchStruct(self, FieldNameItems):
        
        ''' get column field '''
        self.inRequest = self.partofList(FieldNameItems['VariablesRequest'])
        self.outRequest = self.partofList(FieldNameItems['VariablesOut'])
        
        ''' get field type '''
        for inField in self.inRequest:
            reDict = EventSearch().searchFieldType(inField)
            if reDict['Status'] == 'Success':
                for key,value in reDict.items():
                    if key != 'Status':
                        self.getFieldSearchResult[key]=value
            else:
                return reDict['msg']
            
        for outField in self.outRequest:
            reDict = EventSearch().searchFieldType(outField)
            if reDict['Status'] == 'Success':
                for key,value in reDict.items():
                    if key != 'Status':
                        self.getFieldSearchResult[key]=value
            else:
                return reDict['msg']
            
        return self.getFieldSearchResult
     
    ''' This method to get Default variable of table ''' 
    def getDefaultVariable(self, Field):
        
        getDefaultofVariable = EventSearch().searchFieldDefault(Field)
        print getDefaultofVariable
        
    ''' This method to get PYname about gameid '''
    def getPYnameaboutGameid(self, gameid):
        
        getPYname = EventSearch().searchGamelistAboutPYname(gameid)

        return getPYname
     
    ''' be part of string by , and put into list '''    
    def partofList(self, Strings):
        
        tmpList = []
        
        if type(Strings).__name__ == 'str':
            if re.search(r',', Strings):
                tmpList=re.split(',',Strings)
            else:
                tmpList.append(Strings)
        else:
            return 'Strings %s not comfot format' % Strings
        
        return tmpList
    
    ''' get OIDtype by oid from method '''
    def getOidtypebyOID(self, oid):
        
        getOidtype = DataSearch().SearchOIDsimpleName(oid)

        return getOidtype
    
class MainScheduler:
    
    def __init__(self):
        
        self.main = {}
    
    ''' Simply get oid search result '''    
    def searchOID(self, oid):
        
        getSearchResult = EventSearch().searchOIDinTemplate(oid)
        
        return getSearchResult
    
    ''' detail get oid result for whole line '''
    def searchOIDdetail(self, oid):
        
        getSearchDetail = EventSearch().searchOIDdetail(oid)
        
        return getSearchDetail
    
    def searchOIDname(self, oid):
        
        getSearchOIDname = EventSearch().searchOIDdetailinTemplate(oid)
        
        return getSearchOIDname
    
    ''' controller using scheduler '''
    def getAllscheduler(self, oid, Var, varGET, data, useMethod):
        
        ''' thought thres to judge event '''
        getresult = Event().Control(oid, Var, varGET, data, useMethod)
        
        ''' throught warning to decide join Judgement -> multi-event trigger'''
        
        ''' throught judge into database '''
        if getresult == 'Warning':
            
            EventSearch().addintoAlarm('Warning', 0, oid, data, 'test')
            
        elif getresult == False:
            
            EventSearch().addintoAlarm('event', 5, oid, data, 'test')

        return 'Success'
    
    def addIntoAlarm(self, judgeStatus, eventlevel, oid, data):
   
        if judgeStatus == 'Warning':
            
            for key,value in data.items():
                if type(value).__name__ == 'dict':
                    value = changeDict().dicttostr(value)
            
                EventSearch().addintoAlarm('Warning', 0, oid, value, key)
            
        elif judgeStatus == False:
            
            for key,value in data.items():
                if type(value).__name__ == 'unicode' or type(value).__name__ == 'str':           
                    EventSearch().addintoAlarm('event', 4, oid, value, key)
                    
                elif type(value).__name__ == 'dict':
		    # {'percent': {'Status': 'Over', 'hold': '2', 'actual': 3, 'Time': '2013\xe5\xb9\xb403\xe6\x9c\x8821\xe6\x97\xa5_14:54\xe5\x88\x86'}}
		    print "########### value:", value
                    for eachZone, inform in value.items():

	                newGame = '%s-%s' % (key, eachZone)
                        newGame = newGame.encode('utf8')

                        newInform = ""
                        if type(inform).__name__ == 'list':
                            for eachValue in inform:
                                newInform = newInform + str(eachValue) + "|"
			elif type(inform).__name__ == 'dict':
			    newInform = str(inform)
                        
                        EventSearch().addintoAlarm('event', 4, oid, newInform, newGame)
            
        return 'Success'
    
    def readconfig_tableRelation(self, eventType):
        
        count = 0
        tmpValue = ""
        
        getConfig = readFromConfigFile().get_config_tableRelation()
        for key,value in getConfig.items():
            if key == 'tableRelation':
                for eachValue in range(len(value)):
                    if int(value[eachValue][0]) == int(eventType):
                        count = 1
                        tmpValue = value[eachValue][1]
                    
        if count != 0:
            return dict(Status='Success', hold=tmpValue)
        else:
            return dict(Status='False', msg='Not found tableRelation in memory.')
        
    def readconfig_ThresHold(self, eventVar):
        
        count = 0
        
        getconfigVar = readFromConfigFile().get_config_ThresHold()
        for key,value in getconfigVar.items():
            if key == 'ThresHold':
                for eachValue in range(len(value)):
                    if value[eachValue][0] == eventVar:
                        count = 1
                        tmpValue  = value[eachValue][1]
                        
        if count != 0:
            return dict(Status='Success', Return=tmpValue)
        else:
            return dict(Status='False', msg='Not found ThresHold in memory.')
        
    def readconfig_thresCalculation(self, InChar):
        
        getInCHAR = readFromConfigFile().get_config_thresCalculation()
        for key,value in getInCHAR.items():
            if key == 'thresCalculation':
                for eachValue in range(len(value)):
                    if int(value[eachValue][0]) == int(InChar):
                        count = 1
                        tmpValue  = value[eachValue][1]
        if count != 0:
            return dict(Status='Success', Return=tmpValue)
        else:
            return dict(Status='False', msg='Not found thresCalculation in memory.')
    
    ''' This method used to search gameID by gameName '''    
    def searchGameID(self, gameName):
        
        getGameIDdict = EventSearch().searchGameIDbyGamename(gameName)
        
        return getGameIDdict
    
    ''' This method used to search thresNumberID by gameid & thresType '''
    def searchThresNumberID(self, gameid, threstype):
        
        getthresnumberdict = EventSearch().searchThresID(gameid, threstype)
        
        return getthresnumberdict
    
    ''' This method used to search thresNumber Detail '''
    def searchThresDetail(self, thresID):
        
        getThresdetail = EventSearch().searchThresDetail(thresID)
        
        return getThresdetail
    
    ''' 
    This method used to get White List of eachGame could be ignore by searchType 
    example :  ignore  curves of SGZH
    '''
    def searchIgnoreType(self, eventtype, gameID):
        
        getSearchIgnore = EventSearch().searchIgnore(eventtype, gameID)
        
        return getSearchIgnore
    
    ''' This method used to link with time basic method to calc timestamp '''
    def timeBasicCalc(self, timestamp, method=1):
        
        getTime = TimeBasic().timeControl(timestamp, method)

        return getTime
    
class AlarmScheduler:
    
    def __init__(self):
        
        self.returns = ""
        
    def testAlarm(self, OID):
        
        getAlarmReturn = AlarmControl().testAlarm(OID)
        
        return getAlarmReturn
    
    def AlarmControl(self, OID):
        
        getAlarmControlReturn = AlarmControl().AlarmGetdetailControl(OID)
        
        return getAlarmControlReturn
    
class ExplainScheduler:
    
    def __init__(self):
        
        self.returns = ""
    
    def ExplaintoHuman(self, OIDname, ComputerLanguage):
        
        getExplain = HumanRead().ReadtoHuman(OIDname, ComputerLanguage)
        
        return getExplain

class EventScheduler:
    
    def __init__(self):
        
        self.returns = ""
        
    def Searchinformintempprocess(self, ipaddress, process, timestamp):
        
        getSearchResult = EventSearch().tempSearchintempprocess(ipaddress, process, timestamp)
        
        return getSearchResult
    
    def searchdetailinhostname(self, hostname):
        
        getSearchofhostname = EventSearch().searchhostnametoprocess(hostname)
        
        return getSearchofhostname
    
    def searchintempprocess(self, hostname):
        
        getSearchoftempprocess = EventSearch().searchtempprocess(hostname)
        
        return getSearchoftempprocess
    
    def searchzonetohost(self, hostname):
        
        getSearchofzonetohost = EventSearch().searchzonetohost(hostname)
        
        return getSearchofzonetohost
    
    def searchprocessinfo(self, ipaddress):
        
        getSearchresultaboutprocessinfo = DataSearch().getwebprocessinfo(ipaddress)
        
        return getSearchresultaboutprocessinfo
    
    def searchgamelisttoarea(self, zoneID):
        
        getsearchofgamelisttoarea = EventSearch().searchgamelisttoarea(zoneID)
        
        return getsearchofgamelisttoarea
    
    def searchgameNamebygameID(self, gameID):
        
        getsearchofgamename = EventSearch().getGameNamebyGameID(gameID)
        
        return getsearchofgamename