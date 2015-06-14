# -*- coding: utf-8 -*-
''' @author : majian'''
import pdb
import os, sys, re, time
import simplejson as json

''' webService statement '''
import urllib2
import soaplib
from soaplib.core.util.wsgi_wrapper import run_twisted 
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.binary import Attachment
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String,Boolean

from store import StoreinMainServer
from Expand import ExpandStep
from Transport import TransportMain
from officialexpand import OfficialExpand

from BaseClass.logger import LoggerRecord
logger = LoggerRecord().initlog()

from model.cmdbsearch import BasicSearch
from event.Eventanalyst import OidAnalyst
from alarm.Main import AlarmMain
from event.EventMain import EventMain
from alarm.oidrepeat import Repeat
from Control.outside.advertisement import Advertisement
from Control.outside.fastreg import FastRegofPlatform
from BaseClass.timeBasic import TimeBasic
from interface.eventsearch import searchOfevent
from interface.windowsAD import LoginAuthorized
from interface.collection.flushtables import FlushGameName
from BaseClass.verifityDependence import changeDict, base64Data
from BaseClass.MsgPack import MessagePack
from model.dbsearch import DataSearch, EventTransportSearch, EventSearch, AlarmSearch, EventTransportExpand, CircultSearch
from interface.collection.people import NumberofPeople, RealofPeople, HistoryofCurves, NowofCurves

''' ExternalWebservice Usage. '''
# output context class
from Control.struct import C_test, C_loginReback, C_loginInformationReback, C_NowNumberCurves, C_HistoryofCurves, C_EventSearch
# This part for event transport
from Control.struct import C_EventBasicStatus, C_EventGameList, C_EventLevel, C_EventfromEventAlarm, C_UserBelong, C_WholeUsing, C_userSelect, C_TransportMain, C_RecentlyTenEvent, C_designPeople, C_designsearch, C_EventDetailSearch, C_EasyNamefromFullName
# This part for test mainserver database
from Control.struct import C_TestMainserverDatabase, C_testMainServerTable, C_insertJudge, C_searchMaxLine, C_inMaximo, C_careCount, C_EventSearchofDoing, C_ReadfromEventTrace, C_RestoreResultofEasy, C_eventfinishedsearch, C_eventdoingsearchByCombinationParameter, C_eventdoingsearchByCombinationParameterweb, C_eventfinishedByCombinationParameter, C_eventfinishedByCombinationParameterweb
# This part for Alarm module using
from Control.struct import C_AlarmModuleTest, C_AlarmModule
# This part for Event module using
from Control.struct import C_EventModuleTest, C_EventModule

''' OfficialWebservice Usage. '''
from Control.struct import C_counterStatus, C_testUserRegistered, C_webadvertising, C_fastRegtest, C_getRecentlyEvent
# New using for platform php
from Control.struct import C_Cachecounterstatus, C_Cachefastreg, C_CacheofAdvertising, C_operationADurl, C_ServerMaintain, C_ServerhasbeenMaintain, C_curvesofnumberperson

class externalWebservice(DefinitionBase):

    ''' Connect Test for Remote Server'''
    @soap(_returns=C_test)
    def ConnectTest(self):
        Variable = C_test()

        Variable.TestResult = 'Connection test OK.'
        
        return Variable
    
    ''' Company windows AD login method'''
    @soap(String, String, _returns=C_loginReback)
    def webValidateLogin(self, LoginUserName='None', LoginUserPass='None'):
        
        Variable = C_loginReback()
        
        newLoginPass = urllib2.unquote(LoginUserPass)
        
        logger.debug("#### webValidateLogin: username:%s, password:%s" % (LoginUserName, newLoginPass))
        
        getInputDict = dict(loginUserName=LoginUserName, loginPassword=newLoginPass)
        changeLoginStr = changeDict().dicttostr(getInputDict)
        
        getLogin = LoginAuthorized().ADLogin(changeLoginStr)
        if getLogin['Status'] == True:
            Variable.Status = 'Success'
            Variable.ValidateTime = getLogin['validateTime']
        else:
            Variable.Status = 'False'
            Variable.ValidateTime = getLogin['validateTime']
        
        return Variable 
    
    ''' Company windows AD user detail Information '''
    @soap(String, String, _returns=C_loginInformationReback)
    def webValidateLoginInformation(self, LoginUserName='None', LoginUserPass='None'):
        
        Variable = C_loginInformationReback()  
       
        getInputDict = dict(loginUserName=LoginUserName, loginPassword=LoginUserPass)
        changeLoginStr = changeDict().dicttostr(getInputDict)
       
        getLogin = LoginAuthorized().ADLogin(changeLoginStr)
        if getLogin['Status'] == True:
            getLInformation = LoginAuthorized().getUserInformation(getLogin['Username'])
            Variable.Status = 'Success'
            Variable.Mail = getLInformation['Mail']
            Variable.StaffNum = getLInformation['Staffnum']
        else:
            Variable.Status = 'False'
            Variable.Mail = ''
            Variable.StaffNum = ''
            
        return Variable
    
    ''' Company the Number of curves Now '''
    @soap(String, _returns=C_NowNumberCurves)
    def NumberofNowCurves(self, GameName='None'):
        
        Variable = C_NowNumberCurves()
 
        if GameName == 'None':
           
            Variable.Name = 'None'
            Variable.JsonChar = 'Error Input.'
            
        else:
            
            newReturnDict =  NowofCurves().nowController(GameName)
            
            ''' No.3 : change Dict to JSON then return to User '''
            Variable.Name = GameName
            Variable.JsonChar = json.dumps(newReturnDict)
                 
        return Variable
    
    ''' Company of history Curves '''
    @soap(String, Integer, _returns=C_HistoryofCurves)
    def NumberofHistoryCurves(self, GameName='None', Timestamp='None'):
        
        Variable = C_HistoryofCurves()
        
        if GameName == 'None' or Timestamp == 'None':
           
            Variable.Name = 'None'
            Variable.JsonChar = 'Error Input.'
            
        else:
            
            getFromhistory = HistoryofCurves().historyController(GameName, Timestamp)
            del getFromhistory['Status']
            Variable.Name = GameName
            Variable.JsonChar = json.dumps(getFromhistory)
            
        return Variable
    
    ''' Company of test Alarm search '''
    @soap(String, _returns=C_EventSearch)
    def AlarmSearch(self, OID='None'):
        
        Variable = C_EventSearch()
        
        if OID == 'None':
            Variable.JsonChar = 'Error Input.'
        else:        
            searchResult = searchOfevent().searchOID(OID)
            if searchResult['Status'] == 'Success':
                del searchResult['Status']
                
                searchResult = json.dumps(searchResult)
                
                Variable.JsonChar = searchResult
                
        return Variable
        
################################################################
################ This Part of Event Transport ##################
################################################################

    ''' Get Basic Status '''
    @soap(_returns=C_EventBasicStatus)
    def EventTransportofGetBasicStatus(self):
         
        Variable= C_EventBasicStatus()

        getSearchbasic = EventTransportSearch().searchofbasicstatus()
        if getSearchbasic['Status'] == 'Success':
            del getSearchbasic['Status']
            
            Variable.JsonChar = json.dumps(getSearchbasic['basicstatus']) 
        else:
            Variable.JsonChar = json.dumps(getSearchbasic['msg'])
        
        return Variable
    
    ''' Get Basic All GameList '''
    @soap(Integer, _returns=C_EventGameList)
    def EventofGameListAll(self, isUse=1):
        
        try:
            if isUse:
                isUse = isUse
            else:
                isUse = 1
        except NameError:
            isUse = 1

        Variable = C_EventGameList()
        
        getSearchofGameList = EventTransportSearch().searchGameListAll(isUse)
        if getSearchofGameList['Status'] == 'Success':
            del getSearchofGameList['Status']
            
            Variable.JsonChar = json.dumps(getSearchofGameList)
            
        else:
            Variable.JsonChar = json.dumps(getSearchofGameList['msg'])
            
        return Variable
    
    ''' Get EventLevel '''
    @soap(_returns=C_EventLevel)
    def EventLevelofsearch(self):
        
        Variable = C_EventLevel()
        
        getSearchofeventlevel = EventTransportSearch().searcheventlevel()
        if getSearchofeventlevel['Status'] == 'Success':
            del getSearchofeventlevel['Status']
            
            Variable.JsonChar = json.dumps(getSearchofeventlevel['eventlevel'])
            
        else:
            Variable.JsonChar = json.dumps(getSearchofeventlevel['msg'])
            
        return Variable
    
    ''' Get Event from table.eventalarm '''
    @soap(Integer, Integer, _returns=C_EventfromEventAlarm)
    def EventSearchofeventalarm(self, GameID, Grade):
        
        Variable = C_EventfromEventAlarm()
        
        '''
        Step 1. check GameID exist.
        '''
        getCheckGameID = EventSearch().getGameNamebyGameID(GameID)
        if getCheckGameID['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Jsonchar = 'Input GameID not Correct.'
        
        '''
        Step 2. check Grade
        '''     
        getCheckGrade = EventTransportSearch().searcheventlevelexist(Grade)
        if getCheckGrade['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Jsonchar = 'Input eventLevel not Correct.'
            
        '''
        Step 3. select and reback
        '''
        getCheckDictResult = EventTransportSearch().searchEventTrue(GameID, Grade)
        if getCheckDictResult['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Jsonchar = 'MySQL could not found any information about GameID:%s, Level:%s' % (GameID, Grade)
        else:
            del getCheckDictResult['Status']
            Variable.Status = 'Success'
            Variable.Jsonchar = json.dumps(getCheckDictResult)
        
        return Variable
    
    ''' Get User could operation '''
    @soap(String, Integer, _returns=C_UserBelong)
    def UsersOperation(self, username, gameID):
        
        Variable = C_UserBelong()
        
        '''
        Step 1. check user exist.
        '''
        getUsercheck = EventTransportSearch().searchUserExist(username)
        if getUsercheck['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getUsercheck['msg']
            
        '''
        Step 2. check GameID
        '''
        getGameIDcheck = EventSearch().searchGamelistAboutPYname(gameID)
        if getGameIDcheck['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getGameIDcheck['msg']
            
        '''
        Step 3. check user authority
        '''
        # A. from GameID get GroupID
        # Result: GroupID = getGroupIDbyGameID['GroupID']
        getGroupIDbyGameID = EventTransportSearch().searchGroupIDbyGameID(gameID)
        if getGroupIDbyGameID['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getGroupIDbyGameID['msg']
        
        # B. Search UserID from GameGROUP
        getUserIDfromGroup = AlarmSearch().getRelationofUser(getGroupIDbyGameID['GroupID'])
        if getUserIDfromGroup['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getUserIDfromGroup['msg']
        del getUserIDfromGroup['Status']
        
        # C. Search UserName then Expend Compare
        # return : {'Status':'Success', 'operation':'0/1/2'}
        getSureofUser = ExpandStep().compareUser(getUserIDfromGroup, username)
        if getSureofUser['Status'] == 'Success':
            getEventop = EventTransportSearch().searchEventOperation(getSureofUser['operation'])
            if getEventop['Status'] != 'Success':
                Variable.Status = 'False'
                Variable.Char = getEventop['msg']
            else:     
                Variable.Status = 'Success'
                Variable.Char = getEventop['OName'] 
        else:
            Variable.Status = 'False'
            Variable.Char = getSureofUser['msg']    
            
        return Variable   
    
    ''' Event Transport Whole '''
    @soap(Integer, Integer, Integer, _returns=C_WholeUsing)
    def EventTransportWholeUsing(self, GameID, EventLevel, SearchAttitude):
        
        getDict = {}
        Variable = C_WholeUsing()
        
        '''
        Step 1. get all event
        example: { 
                   1L: {
                         'Timestamp': 1363848883L, 
                         'Data': 'tdGVzdCBNaXNzaW5nIFByb2Nlc3M6IENoYXJTZXJ2ZXIxNCcsICdzbWNkJzogJ1pSLUFnZW50LTQueC10ZXN0IE1pc3NpbmcgUHJvY2VzczogQ2hhclNlcnZlcjE0J30='
                       }
                }
        '''
        getSearchofAllevent = EventTransportSearch().searchEventTrue(GameID, EventLevel)
        if getSearchofAllevent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getSearchofAllevent['msg'])
        del getSearchofAllevent['Status']    
        
        '''
        Step 2. search event level
        example: {'Status':'Success'}
                 {'Status':'False', 'msg':''}
        '''
        for key,value in getSearchofAllevent.items():
            getSearchResult = EventTransportSearch().searchCid(key, SearchAttitude)
            if getSearchResult['Status'] == 'Success':
                ''' Step 3. analyst Data && Timestamp '''
                newData = ExpandStep().explainData(value['Data'])
                newTimestamp = ExpandStep().explainTimestamp(value['Timestamp'])
                getDict[key] = dict(Timestamp=newTimestamp, Data=newData)
      
        if len(getDict) != 0:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getDict)
        else:
            msg = 'Could not Match any Result.'
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(msg)
            
        return Variable
    
    ''' user select '''
    @soap(_returns=C_userSelect)
    def userSelect(self):
        
        Variable = C_userSelect()
        
        getStatusofuser = EventTransportSearch().searchUserforSelect()
        if getStatusofuser['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getStatusofuser['msg'])
        else:
            del getStatusofuser['Status']
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getStatusofuser)
            
        return Variable
    
    ''' Event Transport Main '''
    @soap(Integer, Integer, Integer, String, Integer, String, Integer, Integer, _returns=C_TransportMain)
    def EventTransportMain(self, EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark='None', OccurTime=0, deleteornot=0):
        
        Variable = C_TransportMain()
        
        '''
        example :  {'Status': 'Success', 
                    'sourceStatus': 3, 
                    'completeStatus': {
                        'rollback': [-1L], 
                        'equal': [1L], 
                        'next': [3L]
                                    }, 
                    'OtherInform': { 
                        'OccurTime': 1390992139, 
                        'information': 'This is Notefor project', 
                        'opUser': 'majian', 
                        'opTime': '2014-01-20_12:32:21', 
                        'changeStatus': '2 -> 3'
                                   }
                    }
        '''
        getTransportReturn = TransportMain().Main(EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark, OccurTime, deleteornot)
        
        if getTransportReturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.SourceStep = ''
            Variable.CompleteStep = ''
            Variable.Remark = ''
        else:
            Variable.Status = 'Success'
            Variable.SourceStep = getTransportReturn['sourceStatus']
            Variable.CompleteStep = json.dumps(getTransportReturn['completeStatus'])
            Variable.Remark = json.dumps(getTransportReturn['OtherInform'])
            
        return Variable
    
    ''' Recently 10 event '''
    @soap(String, _returns=C_RecentlyTenEvent)
    def getRecentlyTenEvent(self, Order='None'):
        
        Variable = C_RecentlyTenEvent()
        
        location = 0
        
        if type(Order).__name__ == 'NoneType' or Order == 'None' or Order == '':
            Orders = 'All'
            location = 'All'
        elif re.search(r'\d+A', Order):
            Orders = 'After'
            location = re.split('A', Order)[0]
        elif re.search(r'\d+B', Order):
            Orders = 'Before'
            location = re.split('B', Order)[0]
            
        if location == 'All':
            location = location
        elif type(location).__name__ != 'int':
            location = int(location)    
               
        getSearchofEvent = EventTransportSearch().searchRecentlyEvent(Orders, location)
        
        if getSearchofEvent['Status'] != 'Success':
#            Variable.Status = 'False'
            Variable.Recently = json.dumps(getSearchofEvent['msg'])
        elif getSearchofEvent['Status'] == 'Success':
#            Variable.Status = 'Success'
            Variable.Recently = json.dumps(getSearchofEvent['Recently'])
            
        return Variable
    
    ''' get Recently Event. '''
    @soap(String, String, _returns=C_getRecentlyEvent)
    def getRecentlyEventbyweb(self, startpoint, count):
        
        Variable = C_getRecentlyEvent()
        
        if type(startpoint).__name__ == 'NoneType' or startpoint == 'None':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps('input message startpoint Error.')
        
        if type(count).__name__ == 'NoneType' or startpoint == 'None':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps('input message count Error.')
            
        if type(startpoint).__name__ != 'int':
            startpoint = int(startpoint)
        else:
            startpoint = startpoint
            
        if type(count).__name__ != 'int':
            count = int(count)
        else:
            count = count 
           
        getSearchofEvent = EventTransportSearch().searchRecentlyEventbyweb(startpoint, count)
        
        if getSearchofEvent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getSearchofEvent['msg'])
        elif getSearchofEvent['Status'] == 'Success':
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getSearchofEvent['Recently'])
            
        return Variable
        
    ''' add design to people into database '''
    @soap(Integer, Integer, Integer, String, String, String, _returns=C_designPeople)
    def addDesignintodatabase(self, EventID, opTimestamp=0, OccurTime=0, FromUser='None', ToUser='None', EventName='None', NowStatus=0, NextStatus=1, Remark='None', deleteornot=1):
        
        Variable = C_designPeople()
        
        ''' Step 1. check basic input. '''
        # ToUser
        ToUser = ToUser.lower()
        
        # EventName    
        if type(EventName).__name__ != 'NoneType':
            if EventName == '' or EventName == 'None':
                Variable.Status = 'False'
                Variable.Char = 'EventName could not be None.'
                return Variable
            else:
                EventName = base64Data().encode64(EventName)
        else:
            Variable.Status = 'False'
            Variable.Char = 'EventName could not be None.'
            return Variable
        
        # OccurTime
        if type(OccurTime).__name__ == 'NoneType':
            Variable.Status = 'False'
            Variable.Char = 'OccurTime could not be None.'
            return Variable
        else:
            if type(OccurTime).__name__ != 'str':
                OccurTime = str(OccurTime)
                
            if re.search(r'\-',OccurTime):
                OccurTime = TimeBasic().timeRecontrol(OccurTime)
            else:
                OccurTime = int(OccurTime)
        
        # opTimestamp
        if type(opTimestamp).__name__ == 'NoneType':
            Variable.Status = 'False'
            Variable.Char = 'opTimestamp could not be None.'
            return Variable
        else:
            if type(opTimestamp).__name__ != 'str':
                opTimestamp = str(opTimestamp)
                
            if re.search(r'\-',opTimestamp):
                opTimestamp = TimeBasic().timeRecontrol(opTimestamp)
            else:
                opTimestamp = int(opTimestamp)

        ''' Step 2. Add into table.DesigntoOther '''
        Addintotable = EventTransportSearch().addDesginintotable(EventID, opTimestamp, FromUser, ToUser, NowStatus, NextStatus, Remark)
        if Addintotable['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = Addintotable['msg']
            
        ''' Step 3. judge table.eventalarm Exist. '''
        changeEventalarm = EventTransportSearch().changeevent(EventID, NowStatus, NextStatus, EventName, opTimestamp, OccurTime)
        if changeEventalarm['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = changeEventalarm['msg']
        
        ''' Step 4. insert into table.eventrecord. '''
        getintoeventrecord = TransportMain().Main(EventID, NowStatus, NextStatus, ToUser, opTimestamp, Remark, OccurTime, deleteornot)
        if getintoeventrecord['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getintoeventrecord['msg']
        
        Variable.Status = 'Success'
        Variable.Char = 'None'
            
        return Variable
    
    ''' This method use to search design user from people '''
    @soap(String, _returns=C_designsearch)
    def searchDesignUser(self, username):
        
        Variable = C_designsearch()
        
        username = username.lower()
        
        getSearchofDesign = EventTransportSearch().searchUserevent(username)
        if getSearchofDesign['Status'] != 'Success':
            #Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getSearchofDesign['msg'])
        else:
            #Variable.Status = 'Success'
            del getSearchofDesign['Status']
            for key in getSearchofDesign.keys():
                Variable.JsonChar = json.dumps(getSearchofDesign[key])
            
        return Variable
    
    ''' This method used to search event detail from table '''
    @soap(Integer, Integer, _returns=C_EventDetailSearch)
    def searchEventdetail(self, GameID, EventGrade):
        
        ResultDict = {}
        EventIDlist = []
        Variable = C_EventDetailSearch()
        
        ''' Step 1. get EventID (list) '''
        getEventIDList = EventTransportSearch().searchEventIDlist(GameID, EventGrade)
        if getEventIDList['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getEventIDList['msg'])
        else:
            EventIDlist = getEventIDList['EventID']
            
        ''' Step 2. get step by step '''
        for eachEventID in EventIDlist:
            getEachStep = EventTransportSearch().searchStepbyStep(eachEventID)
            getEachResult = EventTransportSearch().searchresultbyresult(eachEventID)
            if getEachStep['Status'] == 'Success':
                ResultDict[eachEventID] = dict(Step=getEachStep['step'])
            else:
                ResultDict[eachEventID] = dict(Step='None')
            ''' Step 3. get result ''' 
            if getEachResult['Status'] == 'Success':
                ResultDict[eachEventID] = dict(ResultDict[eachEventID], **dict(Result=getEachResult['result']))
            else:
                ResultDict[eachEventID] = dict(ResultDict[eachEventID], **dict(Result='None'))
                
        if len(ResultDict) == 0:
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps('Could not found any step in MySQL.')
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(ResultDict)
        
        return Variable
    
    ''' Part of Test Connection with Mainserver '''
    @soap(_returns=C_TestMainserverDatabase)
    def TestMainServerDatabase(self):
        
        Variable = C_TestMainserverDatabase()
        
        getReturnoftestreturn = StoreinMainServer().getTestofMainServer()
        if getReturnoftestreturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getReturnoftestreturn['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = 'None'
            
        return Variable    
    
    ''' Part of test Table exist in MainServer '''
    @soap(String, _returns=C_testMainServerTable)
    def TestMainServerTable(self, inputTable):
        
        Variable = C_testMainServerTable()
        
        checkList = []
        
        if type(inputTable).__name__ != 'str':
            inputTable = str(inputTable)
        
        if re.search(r',', inputTable):
            checkList = re.split(',', inputTable)
        else:
            if len(inputTable) == 0:
                Variable.Status = 'False'
                Variable.JsonChar = json.dumps('input Table Name could not be None')
            else:
                checkList = []
                checkList.append(inputTable)
        
        getReturnofcheckTable = StoreinMainServer().checkTableExistinMainServer(checkList)
        if getReturnofcheckTable['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps('Table Not Exist.')
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps('None')
            
        return Variable
    
    ''' Part of insert into MainServer '''
    @soap(String, String, String, _returns=C_insertJudge)
    def insertMainTable(self, userName, TableName, Content):
        
        Variable = C_insertJudge()
        
        ConList = []
        
        ''' Step 1. split Content. '''
        if re.search(r',', Content):
            ConList = re.split(',', Content)
        
        ''' Step 2. insert into Table '''
        getReturnofinsert = StoreinMainServer().insertintotable(TableName, ConList)
        if getReturnofinsert['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getReturnofinsert['msg'])

        ''' Step 3. insert into Log database '''
        nowtime = int(round(time.time()))
        Content = base64Data().encode64(Content)
        
        getReturnofweblog = EventTransportSearch().insertintoweblog(userName, nowtime, TableName, getReturnofinsert['Status'], Content)
        if getReturnofweblog['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps('Record User Operation Failed.')
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps('None')
            
        return Variable
        
    ''' This part of search max line of each table '''
    @soap(String, _returns=C_searchMaxLine)
    def searchMaxlineoftable(self, tableName):
        
        Variable = C_searchMaxLine()
        
        getsearchMaxReturn = StoreinMainServer().searchtablemaxline(tableName)
        
        if getsearchMaxReturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Count = 'None'
        else:
            Variable.Status = 'Success'
            Variable.Count = getsearchMaxReturn['Count']
            
        return Variable
    
    ''' This part of alarm module (TEST) '''
    @soap(String, Integer, String, Integer, _returns=C_AlarmModuleTest)
    def TestAlarmModuleOutsideUsing(self, Project, Eventlevel, Mbody, Timestamp):
        
        Variable = C_AlarmModuleTest()
        
        TestMessageDict = dict(Project=Project, Eventlevel=Eventlevel, Mbody=Mbody, Timestamp=Timestamp)
        
        getReturnoftestalarm = AlarmMain().alarmManagerTest(TestMessageDict)
        if getReturnoftestalarm['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Info = 'Alarm unifity module Call Failed.'
        else:
            Variable.Status = 'Success'
            Variable.Info = 'None'
            
        return Variable

    ''' This part of alarm module (OFFICIAL) '''
    @soap(String, Integer, String, Integer, _returns=C_AlarmModule)
    def OfficialAlarmModuleOutsideUsing(self, Project, Eventlevel, Mbody, Timestamp):
        
        Variable = C_AlarmModule()
        
        MessageDict = dict(Project=Project, Eventlevel=Eventlevel, Mbody=Mbody, Timestamp=Timestamp)
        
        getReturnofalarm = AlarmMain().alarmManager(MessageDict)
        if getReturnofalarm['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Info = 'Alarm unifity module Call Failed.'
        else:
            Variable.Status = 'Success'
            Variable.Info = 'None'
            
        return Variable
    
    ''' This part of alarm module (OFFICIAL) '''
    @soap(String, Integer, String, Integer, String, _returns=C_AlarmModule)
    def NewOfficialAlarmModuleOutsideUsing(self, Project, Eventlevel, Mbody, Timestamp, Oid):
        
        Variable = C_AlarmModule()
        
        MessageDict = dict(Project=Project, Eventlevel=Eventlevel, Mbody=Mbody, Timestamp=Timestamp, Oid=Oid)
        logger.debug("### getReturnofalarm MessageDict:%s" % MessageDict)
        
        if Oid == '9.0' or Oid == '10.0':
            logger.debug("NewOfficialAlarmModuleOutsideUsing : otherwise with %s" % Oid)
        else:
            getCover = Repeat().searchindatabase(MessageDict)
            logger.debug("### getReturnofalarm getCover:%s" % getCover)
            if getCover['Status'] != 'Success':
                Variable.Status = 'False'
                Variable.Info = '%s, %s, %s, %s Repeat.' % (Project, Mbody, Timestamp, Oid)
                return Variable
        
        getReturnofalarm = AlarmMain().alarmManagerbyoid(MessageDict)
        logger.debug("### getReturnofalarm:%s" % getReturnofalarm)
        if getReturnofalarm['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Info = 'New Alarm unifity module Call Failed.'
        else:
            Variable.Status = 'Success'
            Variable.Info = 'None'
            
        return Variable
    
    ''' This part of Event module (TEST) '''
    @soap(String, String, Integer, String, Integer, Integer, _returns=C_EventModuleTest)
    def TestEventModuleOutsideUsing(self, Eproject, Econtent, Elevel, Eoid, Etimestamp, Econditionid):
        
        Variable = C_EventModuleTest()
        
        EventTestMessageDict = dict(Eproject=Eproject, Econtent=Econtent, Elevel=Elevel, Eoid=Eoid, Etimestamp=Etimestamp, Econditionid=Econditionid)
        
        getReturnoftestEvent = EventMain().TestMainControl(EventTestMessageDict)
        if getReturnoftestEvent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Info = 'Event Control receive module call failed.'
        else:
            Variable.Status = 'Success'
            Variable.Info = 'None'
            
        return Variable
    
    ''' This part of Event module (OFFICIAL) '''
    @soap(String, String, Integer, String, Integer, Integer, _returns=C_EventModule)
    def OfficialEventModuleOutsideUsing(self, Eproject, Econtent, Elevel, Eoid, Etimestamp, Econditionid):
        
        Variable = C_EventModule()
        
        EventMessageDict = dict(Eproject=Eproject, Econtent=Econtent, Elevel=Elevel, Eoid=Eoid, Etimestamp=Etimestamp, Econditionid=Econditionid)
        
        getReturnofEvent = EventMain().MainControl(EventMessageDict)
        if getReturnofEvent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Info = 'Event Control receive module call failed.'
        else:
            Variable.Status = 'Success'
            Variable.Info = 'None'
            
        return Variable
    
    ''' This part of Search in Maximo '''
    @soap(String, _returns=C_inMaximo)
    def searchinMaximoforDetail(self, ipaddress):
        
        Variable = C_inMaximo()
        
        getSearchofResult = EventTransportSearch().searchinassets(ipaddress)
        if getSearchofResult['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getSearchofResult['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getSearchofResult['Detail'])
            
        return Variable
    
    ''' This part is used to add care count '''
    @soap(Integer, String, _returns=C_careCount)
    def addcareofevent(self, EventID, Username):
        
        Ciddetail = 0
        
        Variable= C_careCount()
        
        ''' Step 1. check user care. '''
        getUsernameAttention = EventTransportExpand().searchcarepeople(EventID, Username)
        if getUsernameAttention['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getUsernameAttention['msg']
            return Variable
        
        ''' Step 2. check input '''
        if type(EventID).__name__ != 'int':
            Variable.Status = 'False'
            Variable.Char = 'Input EventID : Not Integer.'
        else:
            getCheck = EventTransportSearch().searcheventidexist(EventID)
            if getCheck['Status'] != 'Success':
                Variable.Status = 'False'
                Variable.Char = getCheck['msg']
                
        ''' Step 3. get Cid '''
        getCid = EventTransportSearch().searchCidfromEid(EventID)
        if getCid['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getCid['msg']
        else:
            Ciddetail = getCid['Cid']
            
        ''' Step 4. add care count '''
        getAdd = EventTransportSearch().addcarecountfromCid(Ciddetail)
        if getAdd['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getAdd['msg']
        
        ''' Step 5. insert into table.carepeopledetail '''
        getintocarepeopledetail = EventTransportExpand().addcarepeopledetail(EventID, Username)
        if getintocarepeopledetail['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getintocarepeopledetail['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = 'None'
            
        return Variable
    
    ''' This part used to search project Easy name from full name. '''
    @soap(String, _returns=C_EasyNamefromFullName)
    def searchNamefromFullNameaboutProject(self, FullName):
        
        Variable = C_EasyNamefromFullName()
        
        getReturn = EventSearch().searchGameNamebyFullname(FullName)
        if getReturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getReturn['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getReturn['Return'])
            
        return Variable
        

    ''' This part will be searched event which be tracing. '''
    @soap(String, String, _returns=C_ReadfromEventTrace)
    def searchdoingEvent(self, GameID, EventGrade):
        
        count = 0

        Variable = C_ReadfromEventTrace()
        
        print "GameID, EventGrade:", GameID, EventGrade
        print "## type:", type(GameID), type(EventGrade)
        
        ''' Step 1. judge input variable. '''
        if type(GameID).__name__ != 'NoneType':
            if GameID == '' or GameID == 'None':
                GameID = 'None'
            else:
                GameID = GameID
        else:
            if GameID == '' or GameID == 'None':
                GameID = 'None'
            else:
                GameID = GameID
        
        if type(EventGrade).__name__ != 'NoneType':
            if EventGrade == '' or EventGrade == 'None':
                EventGrade = 'None'
            else:
                EventGrade = EventGrade
        else:
            if EventGrade == '' or EventGrade == 'None':
                EventGrade = 'None'
            else:
                EventGrade = EventGrade
        
        ''' Step 2. judge input '''       
        if GameID == 'None' and EventGrade == 'None':
            #Variable.Status = 'False'
            Variable.JsonChar = json.dumps('Need At least One Variable for interface.')
            return Variable
        else:
            getReturnofjudgeinput = ExpandStep().searchfromeventdoing(GameID, EventGrade)
            if getReturnofjudgeinput['Status'] != 'Success':
                #Variable.Status = 'False'
                Variable.JsonChar = json.dumps(getReturnofjudgeinput['msg'])
            else:
                #Variable.Status = 'Success'
                if len(getReturnofjudgeinput['Detail']) > 10:
                    getReturnofjudgeinput['Detail'].reverse()
                    length = getReturnofjudgeinput['Detail']
                    Variable.JsonChar = json.dumps(length)
                else:
                    Variable.JsonChar = json.dumps(getReturnofjudgeinput['Detail'])
                
        return Variable
    
    ''' This method used to close event easy.'''
    @soap(Integer, String, Integer, Integer, String, _returns=C_RestoreResultofEasy)
    def RestoreEasyWay(self, EventID, Username, CloseTime=0, DeleteorNot=1, Detail='None'):
        
        Variable = C_RestoreResultofEasy()
        
        getResultofstore = TransportMain().easyinrestore(EventID, Username, CloseTime, DeleteorNot, Detail)
        if getResultofstore['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getResultofstore['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = ''
            
        return Variable
    
    ''' This method used to search finished event. '''
    @soap(String, String, _returns=C_eventfinishedsearch)
    def SearchRestoreEvent(self, GameID='None', Username='None'):
        
        Variable = C_eventfinishedsearch()
        
        getsearchResultofRestore = TransportMain().RestoreEventFinishedProcess(GameID, Username)
        if getsearchResultofRestore['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getsearchResultofRestore['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getsearchResultofRestore['Array'])
            
        return Variable
    
    ''' This method used to search doing event. '''
    @soap(String, _returns=C_eventdoingsearchByCombinationParameter)
    def SearchEventDoingByCombineParameter(self, getVar):
        
        Variable = C_eventdoingsearchByCombinationParameter()
        
        getsearchofResultdoingevent = TransportMain().searchdoingeventofAnySearch(getVar)
        if getsearchofResultdoingevent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getsearchofResultdoingevent['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getsearchofResultdoingevent['Array'])
            
        return Variable
    
    ''' This method used to search doing event for web. '''
    @soap(String, String, _returns=C_eventdoingsearchByCombinationParameterweb)
    def SearchEventDoingByCombineParameterforweb(self, startpoint, count):
        
        Variable = C_eventdoingsearchByCombinationParameterweb()
        
        getsearchofResultdoingevent = TransportMain().searchdoingeventofAnySearchWeb(startpoint, count)
        if getsearchofResultdoingevent['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getsearchofResultdoingevent['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getsearchofResultdoingevent['Array'])
            
        return Variable
    
    ''' This method used to search event finished. '''
    @soap(String, _returns=C_eventfinishedByCombinationParameter)
    def SearchFinishedByCombineParameter(self, getVar):
        
        Variable = C_eventfinishedByCombinationParameter()
        
        getsearchoffinished = TransportMain().searchfinishedofAnySearch(getVar)
        if getsearchoffinished['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getsearchoffinished['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getsearchoffinished['Array'])
            
        return Variable
    
    ''' This method used to search event finished. '''
    @soap(String, String, _returns=C_eventfinishedByCombinationParameterweb)
    def SearchFinishedByCombineParameterweb(self, startpoint, count):
        
        Variable = C_eventfinishedByCombinationParameterweb()
        
        getsearchoffinished = TransportMain().searchfinishedofAnySearchWeb(startpoint, count)
        if getsearchoffinished['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getsearchoffinished['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getsearchoffinished['Array'])
            
        return Variable
    
class OfficialWebservice(DefinitionBase):
    
    ''' This method used to check counter status '''
    @soap(_returns = C_counterStatus)
    def CounterStatus(self):
        
        Variable = C_counterStatus()
        
        tmpPerson = u'侯心刚(13817234504)'
        tmpPersonchange = tmpPerson.encode('utf8')
        
        getCounterofStatus = OfficialExpand().Part_counter()
        if getCounterofStatus['Status'] == 'Success':
            Variable.Status = 'Success'
            Variable.Char = 'None'
            Variable.SolvePerson = 'None'
        elif getCounterofStatus['Status'] == 'Warning':
            Variable.Status = 'Warning'
            Variable.Char = 'still alive %s ipaddress' % getCounterofStatus['count']
            Variable.SolvePerson = tmpPersonchange
        elif getCounterofStatus['Status'] == 'False':
            Variable.Status = 'False'
            Variable.Char = 'Counter ip all broken, please check.'
            Variable.SolvePerson = tmpPersonchange
        
        return Variable  
    
    ''' This method used to test check login. '''
    @soap(Integer, _returns=C_testUserRegistered)
    def TestofUserRegistered(self, StatusAttitude):
        
        Variable = C_testUserRegistered()

        tmpPerson = u'侯心刚(13817234504)'
        tmpPersonchange = tmpPerson.encode('utf8')

        if StatusAttitude == 0:
            Variable.Status = 'False'
            Variable.Char = 'User Registered False : Auto Robot Test Failed.'
            Variable.SolvePerson = tmpPersonchange
        else:
            Variable.Status = 'Success'
            Variable.Char = 'None'
            Variable.SolvePerson = 'None'
        
        return Variable     
    
    ''' 
    This method used to add url for advertisingarrival
    '''
    @soap(String, String, String, String, String, String, _returns=C_webadvertising)
    def advertisingforwebarrival(self, url='None', operation='add', starttime=0, overtime=0, project='0', pagealias='None'):
        
        Variable = C_webadvertising()
        
        # input 
        # add => http://sso.ztgame.com/?ref=tttttt, 2013.04.02_19:00:00, 2013.04.03_19:00:00, add
        # delete => http://sso.ztgame.com/?ref=tttttt, 0, 2013.04.03_19:00:00, delete
        # select => 
        getReturn = Advertisement().getUrloperation(url, operation, starttime, overtime, project, pagealias)
        if getReturn['Status'] == 'Success':
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps('')
        elif getReturn['Status'] == 'False':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getReturn['msg'])
        elif getReturn['Status'] == 'Select':
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getReturn['List'])
            
        return Variable
    
    '''
    This method used to test fastReg in platform
    '''
    @soap(_returns=C_fastRegtest)
    def testPlatformFastReg(self):
        
        Variable = C_fastRegtest()
        
        tmpPerson = u'侯心刚(13817234504)'
        tmpPersonchange = tmpPerson.encode('utf8')
       
        getReturnoftestfastReg = FastRegofPlatform().testPlatformFastReg('testreg')

        if getReturnoftestfastReg['Status'] == 'Success':
            Variable.Status = 'Success'
            Variable.JsonChar = 'None'
            Variable.SolvePerson = 'None'
        elif getReturnoftestfastReg['Status'] == 'False':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getReturnoftestfastReg['msg'])
            Variable.SolvePerson = tmpPersonchange
        elif getReturnoftestfastReg['Status'] == 'Warning':
            Variable.Status = 'Warning'
            Variable.JsonChar = json.dumps(getReturnoftestfastReg['msg'])
            Variable.SolvePerson = tmpPersonchange
        
        return Variable
    
    ''' This method used to search counterstatus. '''
    @soap(_returns = C_Cachecounterstatus)
    def newCacheforcounterStatus(self):
        
        Variable = C_Cachecounterstatus()
        
        getReturnofback = BasicSearch().searchCacheofCounterStatus()
        if getReturnofback['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getReturnofback['msg']
            Variable.SolvePerson = 'None'
        else:
            Variable.Status = getReturnofback['Dict']['Status']
            Variable.Char = getReturnofback['Dict']['Char']
            Variable.SolvePerson = getReturnofback['Dict']['SolvePerson']
            
        return Variable
    
    ''' This method used to search counterstatus. '''
    @soap(_returns = C_Cachefastreg)
    def newCacheforfastreg(self):
        
        Variable = C_Cachefastreg()
        
        getReturnofback = BasicSearch().searchCacheofFastReg()

        if getReturnofback['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getReturnofback['msg']
            Variable.SolvePerson = 'None'
        else:
            Variable.Status = getReturnofback['Dict']['Status']
            Variable.Char = getReturnofback['Dict']['Char']
            Variable.SolvePerson = getReturnofback['Dict']['SolvePerson']
            
        return Variable
    
    ''' This method used to search given advertising. '''
    @soap(String, String, Integer, _returns=C_CacheofAdvertising)
    def newCacheofadvertising(self, project, url, nowtimestamp):
        
        Variable = C_CacheofAdvertising()
        
        getReturnofSearchaboutcache = TransportMain().searchaboutcacheadvertising(project, url, nowtimestamp)

        if getReturnofSearchaboutcache['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.JsonChar = json.dumps(getReturnofSearchaboutcache['msg'])
        else:
            Variable.Status = 'Success'
            Variable.JsonChar = json.dumps(getReturnofSearchaboutcache['newlist'])
            
        return Variable
    
    ''' This method used to add & del advertising url. '''
    @soap(String, String, String, String, String, String, _returns=C_operationADurl)
    def newoperationADurl(self, url='None', project='0',  pagealias='None', operation='add', starttime=0, overtime=0):
        
        Variable = C_operationADurl()
        
        # flush mainserver table
        # use outside cmd : /root/reload 192.168.66.176 reloadCFDB adveertisingarrival
        os.system('/root/reload 192.168.66.176 reloadCFDB adveertisingarrival')
        
        getReturn = Advertisement().decideOperationaboutAD(url, operation, starttime, overtime, project, pagealias)
        if getReturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getReturn['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = 'None'
            
        return Variable
    
    ''' This method used to flush zone maintain status. '''
    @soap(_returns = C_ServerMaintain)
    def autoflushServermaintian(self):
        
        Variable = C_ServerMaintain()
        
        getReturn = TransportMain().FlushTableAboutServerMaintian()
        print " ### autoflushServermaintian:", getReturn
        if getReturn['Status'] != 'Success':
            Variable.Status = 'False'
        else:
            Variable.Status = 'Success'
            
        return Variable
    
    ''' This method used to search zone status. '''
    @soap(String, String, _returns=C_ServerhasbeenMaintain)
    def searchzonemaintianed(self, gamePYname, zonePYname):
        
        Variable = C_ServerhasbeenMaintain()
        
        getreturn = TransportMain().Searchzonehasbeedmaintain(gamePYname, zonePYname)
        if getreturn['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getreturn['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = getreturn['maintian']
            
        return Variable
    
    ''' This method used to flush table about curves of number. '''
    @soap(String, String, String, _returns=C_curvesofnumberperson)
    def flushcurvesofnumber(self, Request="", OID="1.1.6.0.0.1.2.34.21", timePass="5"):
        
        ''' Step 1. initizlaition Variable. '''        
        getNumber = {}
        MergeResult = {}
        curvesResult = {}

        Variable = C_curvesofnumberperson()
        
        newbody = {}
        newbody['Request'] = Request
        newbody['OID'] = OID
        newbody['timePass'] = timePass

        ''' Step 2. from platform get curves of people. '''
        getFromautoAnalyst = OidAnalyst().AnalystTransportData(newbody)
        if getFromautoAnalyst['Status'] == 'Success':
            listofAnalyst = getFromautoAnalyst['deAnalyst']
            for eachlistVar in listofAnalyst:
                for key,value in eachlistVar.items():
                        
                    getNumber = RealofPeople().RealController(value['GameName'], int(value['timePass']))

                    if getNumber['Status'] == 'Success':
                        if value['GameName'] == 'all':
                            MergeResult = getNumber
                            del MergeResult['Status']
                        else:
                            MergeResult[value['GameName']]=getNumber[value['GameName']]
                                
            
        ''' 
        This part change PROJECT NAME to table.GameList 
        and could be recognized by program
        '''
        for key,value in MergeResult.items():
            judgeKey = AlarmSearch().getInfoCheckGameName(key)
            if judgeKey:
                newKey = judgeKey['realName']
                curvesResult[newKey] = value
            else:
                curvesResult[key] = value
  
        curvesResult = MessagePack().packb(curvesResult)
        curvesResult = base64Data().encode64(curvesResult)

        ''' Step 3. insert into database. '''    
        getinsertintotable = CircultSearch().curvesstore(curvesResult, int(time.time()))
        if getinsertintotable['Status'] != 'Success':
            Variable.Status = 'False'
            Variable.Char = getinsertintotable['msg']
        else:
            Variable.Status = 'Success'
            Variable.Char = 'None'
            
        return Variable
