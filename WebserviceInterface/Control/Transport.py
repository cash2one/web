# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import chardet
import urllib2
import pdb

from model.dbsearch import EventTransportSearch, EventTransportExpand, SearchofEventSearch,\
    EventSearch
from BaseClass.timeBasic import TimeBasic
from model.cmdbsearch import BasicSearch
from interface.linkwithauto import linkAuto
from interface.urlop import urloperation
from interface.AMT import ConnectAMT

class TransportMain:
    
    def __init__(self):
        
        self.returns = ""
        
    def Main(self, EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark='None', OccurTime=0, deleteornot=0):
        '''
        Step 1. Special for each
        '''
        if int(nowStatus) == 0:
            if OccurTime == 'None' or type(OccurTime).__name__ == 'NoneType' or int(OccurTime) == 0:
                msg = 'nowStatus is %s, OccurTime could not be <<< None >>>' % nowStatus
                return dict(Status='False', msg=msg)
        elif int(nowStatus) == 10:
            if deleteornot == 'None' or type(deleteornot).__name__ == 'NoneType':
                msg = 'nowStatus is %s, deleteornot could not be <<< None >>>' % nowStatus
                return dict(Status='False', msg=msg)
            elif Remark == 'None' or type(Remark).__name__ == 'NoneType':
                msg = 'nowStatus is %s, Remark could not be <<< None >>>' % nowStatus
                return dict(Status='False', msg=msg)
        else:
            if Remark == 'None' or type(Remark).__name__ == 'NoneType':
                msg = 'nowStatus is %s, Remark could not be <<< None >>>' % nowStatus
                return dict(Status='False', msg=msg)
        
        '''
        Step 2. get transport of back
        example: {'Status': 'Success', 'sourceStatus': 10, 'completeStatus': {'rollback': [-1L], 'equal': [-1L], 'next': [10L]}}
        example: {'Status': 'False', 'msg':''}
        '''
        getSearchofTransport = EventTransportSearch().searcheventtransport(nowStatus, nextStatus)
        if getSearchofTransport['Status'] != 'Success':
            return getSearchofTransport
        
        '''
        Step 3. get Remark
        '''
        RemarkDict = {}
        RemarkDict['opUser'] = opPeople
        RemarkDict['changeStatus'] = "%s -> %s" % (nowStatus, nextStatus)
        RemarkDict['opTime'] = TimeBasic().timeControl(opTimestamp, 3)
        if OccurTime != 'None':
            RemarkDict['OccurTime'] = OccurTime
        if Remark != 'None':
            RemarkDict['information'] = Remark
            
        '''
        Step 4.  splice result -> ResultDicit <type: dict>
        example : ERROR: {'msg': 'nowStatus is 0, OccurTime could not be <<< None >>>', 'Status': 'False'}
                  RIGHT: {'Status': 'Success', 
                          'sourceStatus': 1, 
                          'completeStatus': {'rollback': [-1L], 'equal': [-1L], 'next': [1L]}, 
                          'OtherInform': {  'OccurTime': 1390992129, 
                                            'opUser': 'majian', 
                                            'opTime': '2014-01-20_12:33:01', 
                                            'changeStatus': '0 -> 1'
                                         }
                          }
        '''
        ResultDict = {}
        ResultDict['Status'] = 'Success'
        ResultDict['sourceStatus'] = getSearchofTransport['sourceStatus']
        ResultDict['completeStatus'] = getSearchofTransport['completeStatus']
        ResultDict['OtherInform'] = RemarkDict
        
        '''
        Step 5. record into database
        Part A. Process into table.eventrecord
        Part B. Result into table.eventrestoreresult
      * Part C. Delete whole eventID in table.eventalarm
        '''
        # Part A.
        if int(nowStatus) != 10:
            getAddintoRecords = EventTransportSearch().AddDataintoRecord(EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark, OccurTime, deleteornot)
            if getAddintoRecords['Status'] != 'Success':
                return getAddintoRecords
        # Part B.
        elif int(nowStatus) == 10:
            getAddintorestore = EventTransportSearch().AddRestoreResult(EventID, opPeople, OccurTime, opTimestamp, deleteornot, Remark)
            if getAddintorestore['Status'] != 'Success':
                return getAddintorestore
        # Part C.      
            getDeleteforeventID = EventTransportSearch().deleteEvent(EventID)
            if getDeleteforeventID['Status'] != 'Success':
                return getDeleteforeventID
            
        return ResultDict     
    
    def easyinrestore(self, EventID, Username, CloseTime, DeleteorNot, Detail):

        tmpOccurTime = ""
        tmpGameID = ""
        tmpData = ""
        tmpOid = ""
        
        if type(Detail).__name__ == 'NoneType':
            Detail = 'None'

        try:
            ''' Step 1. check EventID exist. '''
            getSearchofeventidexist = EventTransportExpand().searcheventdoingexist(EventID)
            if getSearchofeventidexist['Status'] != 'Success':
                return getSearchofeventidexist
            else:
                tmpOpTime = getSearchofeventidexist['opTime']
                tmpOccurTime = getSearchofeventidexist['OccurTime']
                tmpGameID = getSearchofeventidexist['GameID']
                tmpData = getSearchofeventidexist['Data']
                tmpOid = getSearchofeventidexist['Oid']
                tmpEventGrade = getSearchofeventidexist['eventGrade']
                
            ''' Step 2. check designtoother. '''
            getSearchofeventidindesigntoother = EventTransportExpand().searcheventindesigntoother(EventID)
            if getSearchofeventidindesigntoother['Status'] != 'Success':
                return getSearchofeventidindesigntoother
            
            ''' Step 3. check into database. '''
            # A. insert into eventfinished
            #addintoeventfinsied(self, Eid, GameID, Data, Oid, CloseTime=0, DeleteorNot=1, Detail='None', Username='None'):
            getaddintofinished = EventTransportExpand().addintoeventfinsied(EventID, tmpGameID, tmpData, tmpOid, tmpOccurTime, CloseTime, DeleteorNot, Detail, Username)
            if getaddintofinished['Status'] != 'Success':
                return getaddintofinished
        
            ''' Step 4. delete eventexist in eventalarmdoing. '''
            getdeleteofexist = EventTransportExpand().deleteeventdoingexist(EventID)
            if getdeleteofexist['Status'] != 'Success':
                return getdeleteofexist
            
            ''' Step 5. delete designtoother '''
            getdesigntother = EventTransportExpand().deletedesigntotherbyEventID(EventID)
            if getdesigntother['Status'] != 'Success':
                return getdesigntother
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success')
    
    def RestoreEventFinishedProcess(self, GameID, Username):
        
        try:
            ''' Step 1. sure 2 variable. '''
            if type(GameID).__name__ == 'NoneType':
                GameID = 'None'
            
            if type(Username).__name__ == 'NoneType':
                Username = 'None'
            
            print "######## ", GameID, Username    
            ''' Step 2. sure operation. '''
            # A. search all and return
            if GameID == 'None' and Username == 'None':
                getReturn = EventTransportExpand().searchineventfinished(GameID, Username, 1)
            # B. Search GameID             
            elif GameID != 'None' and Username == 'None':
                getReturn = EventTransportExpand().searchineventfinished(GameID, Username, 2)
            # C. Search Username
            elif GameID == 'None' and Username != 'None':
                getReturn = EventTransportExpand().searchineventfinished(GameID, Username, 3)
            # D. Search GameID and Username
            elif GameID != 'None' and Username != 'None':
                getReturn = EventTransportExpand().searchineventfinished(GameID, Username, 4)
                        
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return getReturn
    
    def searchdoingeventofAnySearch(self, getVar):
        
        VarA = 'all'
        VarB = 'all'
        
        try:
            if type(getVar).__name__ == 'NoneType' or getVar == 'None':
                VarA = VarA
                VarB = VarB
                
            elif re.search(r'^\dA|^\d+A', getVar):
                VarA = re.split('A',getVar)[0]
                VarB = 'After'
                
            elif re.search(r'^\dB|^\d+B', getVar):
                VarA = re.split('B',getVar)[0]
                VarB = 'Before'
            
            getReturn = SearchofEventSearch().searchofeventdoing(VarA, VarB)
            return getReturn
        
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    def searchdoingeventofAnySearchWeb(self, startpoint, count):
        
        try:
            if type(startpoint).__name__ == 'NoneType' or startpoint == 'None':
                return dict(Status='False', msg='input startpoint error.')
            
            if type(count).__name__ == 'NoneType' or count == 'None':
                return dict(Status='False', msg='input count error.')
                
            if type(startpoint).__name__ != 'int':
                startpoint = int(startpoint)
            else:
                startpoint = startpoint
                
            if type(count).__name__ != 'int':
                count = int(count)
            else:
                count = count
            
            getReturn = SearchofEventSearch().searchofeventdoingWeb(startpoint, count)
            return getReturn
        
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    def searchfinishedofAnySearch(self, getVar):
        
        VarA = 'all'
        VarB = 'all'
        
        try:
            if type(getVar).__name__ == 'NoneType' or getVar == 'None':
                VarA = VarA
                VarB = VarB
                
            elif re.search(r'^\dA|^\d+A', getVar):
                VarA = re.split('A',getVar)[0]
                VarB = 'After'
                
            elif re.search(r'^\dB|^\d+B', getVar):
                VarA = re.split('B',getVar)[0]
                VarB = 'Before'
            
            getReturn = SearchofEventSearch().searchoffinishdoing(VarA, VarB)
            return getReturn
        
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    def searchfinishedofAnySearchWeb(self, startpoint, count):

        try:
            if type(startpoint).__name__ == 'NoneType' or startpoint == 'None':
                return dict(Status='False', msg='input startpoint error.')
            
            if type(count).__name__ == 'NoneType' or count == 'None':
                return dict(Status='False', msg='input count error.')
                
            if type(startpoint).__name__ != 'int':
                startpoint = int(startpoint)
            else:
                startpoint = startpoint
                
            if type(count).__name__ != 'int':
                count = int(count)
            else:
                count = count
            
            getReturn = SearchofEventSearch().searchoffinishdoingweb(startpoint, count)
            return getReturn
        
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    def searchaboutcacheadvertising(self, project, url, nowtimestamp):
        
        if type(project).__name__ == 'NoneType' or project == 'None':
            project = 'None'
            
        if type(url).__name__ == 'NoneType' or url == 'None':
            url = 'None'    
            
        if type(nowtimestamp).__name__ == 'NoneType' or nowtimestamp == 'None':
            nowtimestamp = 0
        
        if project == 'None' and url != 'None':
            getrebackofad = BasicSearch().searchurlinad(url, nowtimestamp)
            return getrebackofad
        elif project != 'None' and url == 'None':
            getrebackofad = BasicSearch().searchprojectinad(project, nowtimestamp)
            return getrebackofad
        elif project != 'None'  and url != 'None':
            getrebackofad = BasicSearch().searchprojectandurlinad(project, url, nowtimestamp)
            return getrebackofad
        else:
            return dict(Status='False', msg='Input Variable Error.')
            
            
    def FlushTableAboutServerMaintian(self):

        ''' 
        Step 1. getallplatform detail. 
        Example : {'Status': 'Success', 
                   'list': [
                   {'gamePYname': '\xc3\x86\xc2\xae\xc3\x83\xc3\xac\xc3\x96\xc2\xae\xc3\x82\xc3\x83', 
                    'zonePYname': '\xc3\x8e\xc3\xb3\xc3\x88\xc3\xab\xc3\x8c\xc3\xac\xc3\x8d\xc2\xa5', 
                    'zonename': 'PM01'
                    },....
                        ]
        '''
        getallplatform = urloperation().analystplatformzonedetail()
        if getallplatform['Status'] != 'Success':
            return getallplatform
        
        
        '''
        Step 2. getallfromamt
        Example : [{'gamePYname': '\xd5\xf7\xcd\xbe\xc3\xe2\xb7\xd1\xb0\xe6', 'ProjectID': '200002', 'gamename': 'ztmfb'}
        '''
        getallfromAMT = ConnectAMT().ProjectSearch()
        
        ''' 
        Step 3. combine information
        TmpDICT: {
                  'Status': 0, 
                  'zonePYname': '\xc2\xb3\xc3\xa0\xc2\xb5\xc3\x98\xc3\x87\xc2\xa7\xc3\x80\xc3\xaf(\xc3\x8d\xc3\xb8\xc3\x8d\xc2\xa8)', 
                  'ProjectID': '200003', 
                  'gamename': 'jr', 
                  'gamePYname': '\xc2\xbe\xc3\x9e\xc3\x88\xc3\x8b', 
                  'zonename': 'TJ84'
                 }
        ''' 
        for eachPlatform in getallplatform['list']:
             
            for eachAMT in getallfromAMT:
                tmpDict = {}
                if eachPlatform['gamePYname'] == eachAMT['gamePYname']:
                    tmpDict['gamePYname'] = eachPlatform['gamePYname']
                    tmpDict['gamename'] = eachAMT['gamename']
                    tmpDict['zonePYname'] = eachPlatform['zonePYname']
                    tmpDict['zonename'] = eachPlatform['zonename']
                    tmpDict['ProjectID'] = eachAMT['ProjectID']
                    tmpStatusResult = linkAuto().linkwithzonedetail(eachPlatform['gamePYname'], eachPlatform['zonePYname'])
                    if tmpStatusResult['Status'] != 'Success':
                        tmpDict['Status'] = 500
                    else:
                        tmpDict['Status'] = tmpStatusResult['maintain']
           
                    getinsertreturn = EventSearch().addintozoneinformamt(tmpDict['gamename'], tmpDict['gamePYname'], tmpDict['zonename'], tmpDict['zonePYname'], tmpDict['Status'])

        return dict(Status='Sucess')
    
    def Searchzonehasbeedmaintain(self, gamePYname, zonePYname):
        
        gamePYname = urllib2.unquote(gamePYname)
        zonePYname = urllib2.unquote(zonePYname)

        getSearchofmaintianed = EventSearch().searchinmaintianlist(gamePYname, zonePYname)
        return getSearchofmaintianed
