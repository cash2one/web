# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys
import pdb

import simplejson as json
from BaseClass.verifityDependence import changeDict, base64Data, changeList
from sqlalchemy import and_, or_, desc
from model import metadata, DBSession, declarativeBase
from BaseClass.timeBasic import TimeBasic

from asset import ASSET
from translate import Translate
from weblog import WebLog
from base import Packtype, Validate, Compress, Encrypt
from commandtype import CommandType, CommandTypeRelation
from curves import CURVES, CurvesIgnore
from gamename import Gameinform
from carepeopledetail import CarePeopleDetail
from oidRelation import OidRequest, OIDVariable
from machinedown import MachineDown
from gamelist import GameList, GameListtoArea, GameGroupRelation
from template import Template
from eventRelation import EventRelation
from eventAlarm import EventAlarm, EventLevel, EventAlarmDoing
from zoneInform import ZonetoHost
from designate import DesigntoOther
from eventtransportdefine import EventTransportDefine
from Eventoperation import EventOperation
from infocheckGamename import InfoCheckGameName
from eventGraderelation import EventGradeRelation
from thresNumber import ThresNumber, ThresRelation
from alarmRelation import ProjecttoGroup, AlarmRelation
from alarmbasic import AlarmGroup, AlarmUser
from EventRecord import EventRecord, EventRestoreResult, EventFinished
from physicalAsset import AgenttoAssets, Ethdetail, EthInfo, HardwareInfo, HosttoId
from process import HostnameToProcess, TempProcess, ProcessStandard
from Eventcircuit import EventCircuitRelation, EventCircultBasic, EventCircultStatus
from responibility import ResonibilityUser, ResponibilityGroup, ResponibilityRelation
from model.assetforagent import AssetidtoEid, AssetForAgent
from model.website.processInfo import ProcessInfo

from model.dbsearch import EventSearch, EventTransportExpand

class Expand:
    
    def searchdoingeventofall(self):
        
        tmpArray = []
        
        try:
            getsearchofdoingeventall = DBSession.query(EventAlarmDoing).order_by(desc(EventAlarmDoing.Eid)).all()
            
            if getsearchofdoingeventall:
                if len(getsearchofdoingeventall) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchofdoingeventall[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchofdoingeventall[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchofdoingeventall[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # EventName
                        newEventName = base64Data().decode64(getsearchofdoingeventall[eachline].EventName)
                        
                        # opTime
                        tmpOpTime = getsearchofdoingeventall[eachline].Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = getsearchofdoingeventall[eachline].OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(getsearchofdoingeventall[eachline].Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = getsearchofdoingeventall[eachline].Eid, GameID = getsearchofdoingeventall[eachline].GameID, GamePYname = GamePYname, Oid = getsearchofdoingeventall[eachline].Oid, OidPYname = OidPYname, eventGrade = getsearchofdoingeventall[eachline].eventGrade, Data = newData, EventName = newEventName))
                else:
                    for eachline in getsearchofdoingeventall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData) 
                        
                        # EventName
                        newEventName = base64Data().decode64(eachline.EventName)
                        
                        # opTime
                        tmpOpTime = eachline.Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = eachline.OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(eachline.Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, eventGrade = eachline.eventGrade, Data = newData, EventName = newEventName))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventalarmdoing.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchdoingeventofallforweb(self, startpoint, count):
        
        tmpArray = []
        
        try:
            getsearchofdoingeventall = DBSession.query(EventAlarmDoing).order_by(desc(EventAlarmDoing.Eid)).all()
            
            if getsearchofdoingeventall:
                if len(getsearchofdoingeventall) > count:
                    for eachline in range(count):
                        tmpThispointer = int(startpoint + eachline)
                        
                        if tmpThispointer < len(getsearchofdoingeventall):
                        
                            # GamePYname
                            tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchofdoingeventall[tmpThispointer].GameID)
                            if tmpGamePYname['Status'] != 'Success':
                                GamePYname = 'None'
                            else:
                                GamePYname = tmpGamePYname['FullName']
                            
                            # OidPYname
                            tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchofdoingeventall[tmpThispointer].Oid)
                            if tmpOidPYname['Status'] != 'Success':
                                OidPYname = 'None'
                            else:
                                OidPYname = tmpOidPYname['TemplateName']
                            
                            # Data
                            newData = base64Data().decode64(getsearchofdoingeventall[tmpThispointer].Data)
                            newData = eval(newData)
                            newData = json.dumps(newData)    
                            
                            # EventName
                            newEventName = base64Data().decode64(getsearchofdoingeventall[tmpThispointer].EventName)
                            
                            # opTime
                            tmpOpTime = getsearchofdoingeventall[tmpThispointer].Timestamp
                            tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                            
                            # OccurTime
                            tmpOccurTime = getsearchofdoingeventall[tmpThispointer].OccurTime
                            tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                            
                            # ToUser
                            tmpUser = EventTransportExpand().searcheventindesigntoother(getsearchofdoingeventall[tmpThispointer].Eid)
                            if tmpUser['Status'] == 'Success':
                                tmpOpuser = tmpUser['ToUser']
                            else:
                                tmpOpuser = 'None'
                            
                            tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = getsearchofdoingeventall[tmpThispointer].Eid, GameID = getsearchofdoingeventall[tmpThispointer].GameID, GamePYname = GamePYname, Oid = getsearchofdoingeventall[tmpThispointer].Oid, OidPYname = OidPYname, eventGrade = getsearchofdoingeventall[tmpThispointer].eventGrade, Data = newData, EventName = newEventName))
                else:
                    for eachline in getsearchofdoingeventall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData) 
                        
                        # EventName
                        newEventName = base64Data().decode64(eachline.EventName)
                        
                        # opTime
                        tmpOpTime = eachline.Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = eachline.OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(eachline.Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, eventGrade = eachline.eventGrade, Data = newData, EventName = newEventName))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventalarmdoing.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchdoingeventofafter(self, startpoint):
        
        tmpArray = []

        if type(startpoint).__name__ != 'int':
            startpoint = int(startpoint)
        
        try:
            getsearchofdoingeventofafter = DBSession.query(EventAlarmDoing).filter((EventAlarmDoing.Eid > startpoint)).order_by(desc(EventAlarmDoing.Eid)).all()
            
            if getsearchofdoingeventofafter:
                if len(getsearchofdoingeventofafter) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchofdoingeventofafter[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchofdoingeventofafter[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchofdoingeventofafter[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # EventName
                        newEventName = base64Data().decode64(getsearchofdoingeventofafter[eachline].EventName)
                        
                        # opTime
                        tmpOpTime = getsearchofdoingeventofafter[eachline].Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = getsearchofdoingeventofafter[eachline].OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(getsearchofdoingeventofafter[eachline].Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = getsearchofdoingeventofafter[eachline].Eid, GameID = getsearchofdoingeventofafter[eachline].GameID, GamePYname = GamePYname, Oid = getsearchofdoingeventofafter[eachline].Oid, OidPYname = OidPYname, eventGrade = getsearchofdoingeventofafter[eachline].eventGrade, Data = newData, EventName = newEventName))
                else:
                    for eachline in getsearchofdoingeventofafter:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # EventName
                        newEventName = base64Data().decode64(eachline.EventName)
                        
                        # opTime
                        tmpOpTime = eachline.Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = eachline.OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(eachline.Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, eventGrade = eachline.eventGrade, Data = newData, EventName = newEventName))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventalarmdoing.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchdoingeventofbefore(self, startpoint):
        
        tmpArray = []
        
        if type(startpoint).__name__ != 'int':
            startpoint = int(startpoint)
        
        try:
            getsearchofdoingeventofbefore = DBSession.query(EventAlarmDoing).filter((EventAlarmDoing.Eid < startpoint)).order_by(desc(EventAlarmDoing.Eid)).all()
            
            if getsearchofdoingeventofbefore:
                if len(getsearchofdoingeventofbefore) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchofdoingeventofbefore[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchofdoingeventofbefore[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchofdoingeventofbefore[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # EventName
                        newEventName = base64Data().decode64(getsearchofdoingeventofbefore[eachline].EventName)
                        
                        # opTime
                        tmpOpTime = getsearchofdoingeventofbefore[eachline].Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = getsearchofdoingeventofbefore[eachline].OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(getsearchofdoingeventofbefore[eachline].Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = getsearchofdoingeventofbefore[eachline].Eid, GameID = getsearchofdoingeventofbefore[eachline].GameID, GamePYname = GamePYname, Oid = getsearchofdoingeventofbefore[eachline].Oid, OidPYname = OidPYname, eventGrade = getsearchofdoingeventofbefore[eachline].eventGrade, Data = newData, EventName = newEventName))
                else:
                    for eachline in getsearchofdoingeventofbefore:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # EventName
                        newEventName = base64Data().decode64(eachline.EventName)
                        
                        # opTime
                        tmpOpTime = eachline.Timestamp
                        tmpOpPYTime = TimeBasic().timeControl(tmpOpTime, 5)
                        
                        # OccurTime
                        tmpOccurTime = eachline.OccurTime
                        tmpOccurPYTime = TimeBasic().timeControl(tmpOccurTime, 5)
                        
                        # ToUser
                        tmpUser = EventTransportExpand().searcheventindesigntoother(eachline.Eid)
                        if tmpUser['Status'] == 'Success':
                            tmpOpuser = tmpUser['ToUser']
                        else:
                            tmpOpuser = 'None'
                        
                        tmpArray.append(dict(OperationTime = tmpOpTime, OperationPYTime = tmpOpPYTime, OccurTime = tmpOccurTime, OccurPYTime = tmpOccurPYTime, opUser = tmpOpuser, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, eventGrade = eachline.eventGrade, Data = newData, EventName = newEventName))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventalarmdoing.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchfinisheddoingeventofall(self):
        
        tmpArray = []
        
        try:
            getsearchfinisheddoingeventofall = DBSession.query(EventFinished).order_by(desc(EventFinished.Eid)).all()
            
            if getsearchfinisheddoingeventofall:
                if len(getsearchfinisheddoingeventofall) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchfinisheddoingeventofall[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchfinisheddoingeventofall[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchfinisheddoingeventofall[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)
                        
                        # Timestamp
                        closeTime = getsearchfinisheddoingeventofall[eachline].CloseTime
                        newclosetime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].CloseTime, 5)
                        
                        # OccurTime
                        occurTime = getsearchfinisheddoingeventofall[eachline].OccurTime
                        newoccurTime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(getsearchfinisheddoingeventofall[eachline].OccurTime, getsearchfinisheddoingeventofall[eachline].CloseTime)
                        
                        # username
                        username = getsearchfinisheddoingeventofall[eachline].Username
                        
                        # close information
                        Detail = getsearchfinisheddoingeventofall[eachline].Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = getsearchfinisheddoingeventofall[eachline].Eid, GameID = getsearchfinisheddoingeventofall[eachline].GameID, GamePYname = GamePYname, Oid = getsearchfinisheddoingeventofall[eachline].Oid, OidPYname = OidPYname, Data = newData))
                else:
                    for eachline in getsearchfinisheddoingeventofall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # Timestamp
                        closeTime = eachline.CloseTime
                        newclosetime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        
                        # OccurTime
                        occurTime = eachline.OccurTime
                        newoccurTime = TimeBasic().timeControl(eachline.OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        # username
                        username = eachline.Username
                        
                        # close information
                        Detail = eachline.Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, Data = newData))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventfinshed.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchfinisheddoingeventofallweb(self, startpoint, count):
        
        tmpArray = []
        
        try:
            getsearchfinisheddoingeventofall = DBSession.query(EventFinished).order_by(desc(EventFinished.Eid)).all()
            
            if getsearchfinisheddoingeventofall:
                if len(getsearchfinisheddoingeventofall) > count:
                    for eachline in range(count):
                        tmpThispointer = int(startpoint + eachline) 
                        
                        if tmpThispointer < len(getsearchfinisheddoingeventofall):
                        
                            # GamePYname
                            tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchfinisheddoingeventofall[tmpThispointer].GameID)
                            if tmpGamePYname['Status'] != 'Success':
                                GamePYname = 'None'
                            else:
                                GamePYname = tmpGamePYname['FullName']
                            
                            # OidPYname
                            tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchfinisheddoingeventofall[tmpThispointer].Oid)
                            if tmpOidPYname['Status'] != 'Success':
                                OidPYname = 'None'
                            else:
                                OidPYname = tmpOidPYname['TemplateName']
                            
                            # Data
                            newData = base64Data().decode64(getsearchfinisheddoingeventofall[tmpThispointer].Data)
                            newData = eval(newData)
                            newData = json.dumps(newData)
                            
                            # Timestamp
                            closeTime = getsearchfinisheddoingeventofall[tmpThispointer].CloseTime
                            newclosetime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[tmpThispointer].CloseTime, 5)
                            
                            # OccurTime
                            occurTime = getsearchfinisheddoingeventofall[tmpThispointer].OccurTime
                            newoccurTime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[tmpThispointer].OccurTime, 5)
                            
                            # DealTime
                            tmpDealTime = TimeBasic().TimeMinus(getsearchfinisheddoingeventofall[tmpThispointer].OccurTime, getsearchfinisheddoingeventofall[tmpThispointer].CloseTime)
                            
                            # username
                            username = getsearchfinisheddoingeventofall[tmpThispointer].Username
                            
                            # close information
                            Detail = getsearchfinisheddoingeventofall[tmpThispointer].Detail
                            
                            tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = getsearchfinisheddoingeventofall[tmpThispointer].Eid, GameID = getsearchfinisheddoingeventofall[tmpThispointer].GameID, GamePYname = GamePYname, Oid = getsearchfinisheddoingeventofall[tmpThispointer].Oid, OidPYname = OidPYname, Data = newData))
                else:
                    for eachline in getsearchfinisheddoingeventofall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # Timestamp
                        closeTime = eachline.CloseTime
                        newclosetime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        
                        # OccurTime
                        occurTime = eachline.OccurTime
                        newoccurTime = TimeBasic().timeControl(eachline.OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        # username
                        username = eachline.Username
                        
                        # close information
                        Detail = eachline.Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, Data = newData))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventfinshed.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchfinisheddoingeventofafter(self, startpoint):
        
        tmpArray = []
        
        if type(startpoint).__name__ != 'int':
            startpoint = int(startpoint)
            
        try:
            getsearchfinisheddoingeventofall = DBSession.query(EventFinished).filter((EventFinished.Eid > startpoint)).order_by(desc(EventFinished.Eid)).all()
            
            if getsearchfinisheddoingeventofall:
                if len(getsearchfinisheddoingeventofall) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchfinisheddoingeventofall[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchfinisheddoingeventofall[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchfinisheddoingeventofall[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # Timestamp
                        closeTime = getsearchfinisheddoingeventofall[eachline].CloseTime
                        newclosetime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].CloseTime, 5)
                        
                        # OccurTime
                        occurTime = getsearchfinisheddoingeventofall[eachline].OccurTime
                        newoccurTime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(getsearchfinisheddoingeventofall[eachline].OccurTime, getsearchfinisheddoingeventofall[eachline].CloseTime)
                        
                        # username
                        username = getsearchfinisheddoingeventofall[eachline].Username
                        
                        # close information
                        Detail = getsearchfinisheddoingeventofall[eachline].Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = getsearchfinisheddoingeventofall[eachline].Eid, GameID = getsearchfinisheddoingeventofall[eachline].GameID, GamePYname = GamePYname, Oid = getsearchfinisheddoingeventofall[eachline].Oid, OidPYname = OidPYname, Data = newData))
                else:
                    for eachline in getsearchfinisheddoingeventofall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # Timestamp
                        closeTime = eachline.CloseTime
                        newclosetime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        
                        # OccurTime
                        occurTime = eachline.OccurTime
                        newoccurTime = TimeBasic().timeControl(eachline.OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        # username
                        username = eachline.Username
                        
                        # close information
                        Detail = eachline.Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, Data = newData))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventfinshed.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def searchfinisheddoingeventofbefore(self, startpoint):
        
        tmpArray = []
        
        if type(startpoint).__name__ != 'int':
            startpoint = int(startpoint)
            
        try:
            getsearchfinisheddoingeventofall = DBSession.query(EventFinished).filter((EventFinished.Eid < startpoint)).order_by(desc(EventFinished.Eid)).all()
            
            if getsearchfinisheddoingeventofall:
                if len(getsearchfinisheddoingeventofall) > 10:
                    for eachline in range(10):
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(getsearchfinisheddoingeventofall[eachline].GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(getsearchfinisheddoingeventofall[eachline].Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(getsearchfinisheddoingeventofall[eachline].Data)
                        newData = eval(newData)
                        newData = json.dumps(newData)    
                        
                        # Timestamp
                        closeTime = getsearchfinisheddoingeventofall[eachline].CloseTime
                        newclosetime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].CloseTime, 5)
                        
                        # OccurTime
                        occurTime = getsearchfinisheddoingeventofall[eachline].OccurTime
                        newoccurTime = TimeBasic().timeControl(getsearchfinisheddoingeventofall[eachline].OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(getsearchfinisheddoingeventofall[eachline].OccurTime, getsearchfinisheddoingeventofall[eachline].CloseTime)
                        
                        # username
                        username = getsearchfinisheddoingeventofall[eachline].Username
                        
                        # close information
                        Detail = getsearchfinisheddoingeventofall[eachline].Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = getsearchfinisheddoingeventofall[eachline].Eid, GameID = getsearchfinisheddoingeventofall[eachline].GameID, GamePYname = GamePYname, Oid = getsearchfinisheddoingeventofall[eachline].Oid, OidPYname = OidPYname, Data = newData))
                else:
                    for eachline in getsearchfinisheddoingeventofall:
                        
                        # GamePYname
                        tmpGamePYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpGamePYname['Status'] != 'Success':
                            GamePYname = 'None'
                        else:
                            GamePYname = tmpGamePYname['FullName']
                        
                        # OidPYname
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            OidPYname = 'None'
                        else:
                            OidPYname = tmpOidPYname['TemplateName']
                        
                        # Data
                        newData = base64Data().decode64(eachline.Data) 
                        newData = eval(newData)
                        newData = json.dumps(newData)   
                        
                        # Timestamp
                        closeTime = eachline.CloseTime
                        newclosetime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        
                        # OccurTime
                        occurTime = eachline.OccurTime
                        newoccurTime = TimeBasic().timeControl(eachline.OccurTime, 5)
                        
                        # DealTime
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        # username
                        username = eachline.Username
                        
                        # close information
                        Detail = eachline.Detail
                        
                        tmpArray.append(dict(occurTime = occurTime, occurPYtime = newoccurTime, DealTime = tmpDealTime, closeTime = closeTime, closePYtime = newclosetime, Username = username, CloseDetail=Detail, Eid = eachline.Eid, GameID = eachline.GameID, GamePYname = GamePYname, Oid = eachline.Oid, OidPYname = OidPYname, Data = newData))
            else:
                return dict(Status='False', msg='MySQL could not found any thing in Eventfinshed.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)