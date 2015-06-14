# -*- coding: utf-8 -*-
''' @author : majian'''


''' use to search information in database'''

import os, re
import sys
import pdb
import chardet
from BaseClass.verifityDependence import changeDict, base64Data, changeList
from sqlalchemy import and_, or_, desc
from model import metadata, DBSession, declarativeBase
from BaseClass.timeBasic import TimeBasic

from BaseClass.logger import LoggerRecord
logger = LoggerRecord().initlog()

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
from zoneInform import ZonetoHost, ZoneInformByAMT
from designate import DesigntoOther
from curvesofpeoplestore import CurvesOfpeopleStore
from eventtransportdefine import EventTransportDefine
from Eventoperation import EventOperation
from infocheckGamename import InfoCheckGameName
from eventGraderelation import EventGradeRelation
from thresNumber import ThresNumber, ThresRelation
from alarmRelation import ProjecttoGroup, AlarmRelation
from alarmbasic import AlarmGroup, AlarmUser
from oidrepeat import OidRepeat, OidControlTime
from EventRecord import EventRecord, EventRestoreResult, EventFinished
from physicalAsset import AgenttoAssets, Ethdetail, EthInfo, HardwareInfo, HosttoId
from process import HostnameToProcess, TempProcess, ProcessStandard
from Eventcircuit import EventCircuitRelation, EventCircultBasic, EventCircultStatus
from responibility import ResonibilityUser, ResponibilityGroup, ResponibilityRelation
from model.assetforagent import AssetidtoEid, AssetForAgent
from model.website.processInfo import ProcessInfo

class DataSearch:
    
    def __init__(self):
        
        self.oidtype = {}
    
    def getPackType(self, compress, encrypt, validate):
        
        getSearchPacktype = DBSession.query(Packtype).filter(and_(Packtype.compress == compress, Packtype.encrypt == encrypt, Packtype.validate == validate)).first()
            
        if getSearchPacktype:
            return int(getSearchPacktype.packtype) 
        else:  
            msg = "SqlAlchemy Error : MySQL packtype_compress_encrypt has not exist search line in compress && encrypt."
            return msg
        
    def checkPackType(self, packtype):
        
        self.reDict = {}
        print "checkPackType : %s" % packtype  
        
        getResultPacktype = DBSession.query(Packtype).filter_by(packtype = packtype).first()
        
        if getResultPacktype:
            self.reDict['compress'] = getResultPacktype.compress
            self.reDict['encrypt'] = getResultPacktype.encrypt
            self.reDict['validate'] = getResultPacktype.validate
        else:
            msg = 'MySQL could not found PackType in table.packtype_compress_encrypt.'
            return msg
        
        return self.reDict
    
    def getCommandtype(self, commandtype):
        
        self.commandtype = {}
        
        getResultCommandtype = DBSession.query(CommandType).filter_by(command = commandtype).first()
        
        if getResultCommandtype:
            self.commandtype['id'] = getResultCommandtype.id
            self.commandtype['command_type'] = getResultCommandtype.command_type
        else:
            msg = 'MySQL could not found CommandType in table.command_type.'
            return msg
        
        return self.commandtype
    
    def getwebprocessinfo(self, ipaddress):
        
        tmpprocessinfo = {}
        
        try:
            getSearchofprocessinfo = DBSession.query(ProcessInfo).filter_by(ip=ipaddress).all()
            
            if getSearchofprocessinfo:
                for eachline in getSearchofprocessinfo:
                    tmpprocessinfo[eachline.name] = eachline.count
            else:
                msg = 'MySQL could not found any information about processinfo.'
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            return dict(Status='False', msg=e)
        
        return dict(Status='Success', processinfo=tmpprocessinfo)
    
    def getCommandRelation_ClienttoServer(self, clientID):
        
        self.ClienttoServer = ""
        
        getClienttoServer = DBSession.query(CommandTypeRelation).filter_by(clientID = clientID).first()
        
        if getClienttoServer:
            self.ClienttoServer = getClienttoServer.serverID
        else:
            msg = 'MySQL could not found serverID in table.command_type_relation'
            return msg
        
        return self.ClienttoServer
    
    def getCommandRelation_ServerCommand(self, serverID):
        
        self.ServerCommand = ""
        
        getServertoClient = DBSession.query(CommandType).filter_by(id = serverID).first()
        
        if getServertoClient:
            self.ServerCommand = getServertoClient.command
        else:
            msg = 'MySQL could not found serverCommand in table.command_type'
            return msg
        
        return self.ServerCommand
    
    def getValidate(self, vid):
        
        self.getValidateResult = ""
        
        getResultValidate = DBSession.query(Validate).filter_by(id = vid).first()
        
        if getResultValidate:
            self.getValidateResult = getResultValidate.id
        else:
            msg = 'MySQL could not found validate in table.validation'
            return msg
        
        return self.getValidateResult
    
    def getCompress(self, compress):
        
        self.getCompressResult = ''
        
        getResultCompress = DBSession.query(Compress).filter_by(compressID = compress).first()
        
        if getResultCompress:
            self.getCompressResult = getResultCompress.id
        else:
            msg = 'MySQL could not found compress in table.compress'
            return msg
        
        return self.getCompressResult
    
    def getEncrypt(self, encrypt):
        
        self.getEncryptResult = ''
        
        getResultEncrypt = DBSession.query(Encrypt).filter_by(encryptID = encrypt).first()
        
        if getResultEncrypt:
            self.getEncryptResult = getResultEncrypt.id
        else:
            msg = 'MySQL could not found encrypt in table.encrypt'
            return msg
        
        return self.getEncryptResult
    def sureCompressEncryptValidate(self, compress, encrypt, validate):
        
        getSearchPacktype = DBSession.query(Packtype).filter(and_(Packtype.compress == compress, Packtype.encrypt == encrypt, Packtype.validate == validate)).first()
            
        if getSearchPacktype:
            return 'success'
        else:  
            msg = "SqlAlchemy Error : MySQL packtype_compress_encrypt has not exist search line in compress && encrypt."
            return msg
        
    def sureGameNameinTable(self, gameName):
        
        getSearchofGamename = DBSession.query(Gameinform).filter_by(gameName = gameName).first()
        
        if getSearchofGamename:
            return 'success'
        else:
            msg = 'SqlAlchemy Error : MySQL gamename has not exist this gameName of %s' % gameName
            return msg
    
    '''
    This method is used to get TemplateType by oid in table.template
    '''    
    def SearchOIDsimpleName(self, oid):
        
        try:
            getSimpleName = DBSession.query(Template).filter_by(OID=oid).first()
            
            if getSimpleName:
                self.oidtype['Status'] = 'Success'
                self.oidtype['TemplateType'] = getSimpleName.TemplateType
            else:
                self.oidtype['Status'] = 'False'
                self.oidtype['msg'] = 'MySQL could not found oid type in table.template.'
                
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return self.oidtype
    
    def searcheachstatus(self, statusid):
        
        try:
            getSearchofstatus = DBSession.query(EventCircultStatus).filter_by(StatusID = statusid).first()
            
            if getSearchofstatus:
                return dict(Status='Success', StatusDesc=getSearchofstatus.StatusDesc)
            else:
                return dict(Status='False', msg='MySQL could not found status id in database.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
            
class LogicSearch:
    
    def getCommandCheck(self, command):
        
        self.getCmdResult = {}
        
        getResultCmd = DBSession.query(CommandType).filter_by(command = command).first()
        
        if getResultCmd:
            self.getCmdResult['id'] = getResultCmd.id
            self.getCmdResult['command'] = getResultCmd.command 
            self.getCmdResult['command_type'] = getResultCmd.command_type
        else:
            msg = 'MySQL could not found command in table.CommandType.'
            return msg
        
        return self.getCmdResult
    
    def getSearchCurves(self):
        
        self.curvesReturn = {}
        
        try:
            getCurves = DBSession.query(CURVES).all()
        
            for eachCurves in range(len(getCurves)):
                self.curvesReturn[getCurves[eachCurves].id] = dict(name=getCurves[eachCurves].name, host=getCurves[eachCurves].host, port=getCurves[eachCurves].port, dbname=getCurves[eachCurves].database)
        
        except Exception, e:
            return e
        
        return self.curvesReturn
    
    def getSearchCurvesByVariable(self, gameName):
        
        self.getSearchResult = {}
        
        try:
            getCurves = DBSession.query(CURVES).filter_by(name=gameName).first()
            
            if getCurves:
                self.getSearchResult[getCurves.id] = dict(name=getCurves.name, host=getCurves.host, port=getCurves.port, dbname=getCurves.database)    
            else:
                return 'MySQLdb: no rows selected in table.curves'

        except Exception, e:
            return e

        return self.getSearchResult
    
class TranslateSearch:
    
    def getsimpleTranslate(self, simple):
        
        self.getallResult = {}
        
        try:
            getAllsearch = DBSession.query(Translate).filter_by(simple = simple).first()
        
            if getAllsearch:
                self.getallResult['id'] = getAllsearch.id
                self.getallResult['detail'] = getAllsearch.detail
                
            else:
                msg = 'MySQL could not found simple in table.translate'
                return msg
            
            return dict(Status='success', searchResult=self.getallResult)
        
        except Exception, e:
            return e   
        
class EventSearch:
    
    def __init__(self):
        
        self.oidexist = {}
        self.fieldtype = {}
        self.fieldefault = {}
        self.PYname = {}
        self.Gid = {}
        self.gameName = {}
        self.templateDict = {}
        self.oidDetail = {}
        self.templateOIDdetail = {}
        self.thresID = {}
        self.thresDetail = {}
        self.typeIgnore = {}
        self.searchtmp = {}
        self.zonetohost = {}
        self.searchhostname = {}
        self.searchTempprocess = {}
        self.gamelisttoarea = {}
    
    def SearchoidRepeat(self, content, oid, Nowtime):
        
        Overtime = 0
        
        if type(content).__name__ == 'dict':
            content = str(content)
        
        try:
            getSearchinoidrepeat = DBSession.query(OidRepeat).filter(and_(OidRepeat.content == content, OidRepeat.oid == oid)).order_by(desc(OidRepeat.timestamp)).first()
            
            if getSearchinoidrepeat:
                ''' Search time over Overtime. '''
                getOvertime = self.searchoidovertime(oid)
                if getOvertime:
                    Overtime = getOvertime['Overtime']
                else:
                    return dict(Status='False', msg='Content has oid Repeat Define.')
                
                ''' Compare Time PASS. '''
                if ((int(int(Nowtime) - int(getSearchinoidrepeat.timestamp))) > Overtime):
                    getReturnofnewadd = self.addintooidrepeat(content, oid, Nowtime)
                    if getReturnofnewadd['Status'] == 'Success':
                        return dict(Status='Success')
                    else:
                        return getReturnofnewadd
                else:
                    ''' flush time pass. '''
                    getSearchinoidrepeat.timestamp = Nowtime
                    DBSession.commit()
                    return dict(Status='False', msg='Flush Table OidRepeat.')
            else:
                ''' add new line into database. '''
                getReturnofadd = self.addintooidrepeat(content, oid, Nowtime)
                if getReturnofadd['Status'] == 'Success':
                    return dict(Status='Success')
                else:
                    return getReturnofadd
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
  
        DBSession.commit()
        
    def addintooidrepeat(self, content, oid, Nowtime):
        
        try:
            DBSession.add(OidRepeat(content, oid, Nowtime))
            
            DBSession.commit()
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success')

    def searchoidovertime(self, oid):
        
        try:
            getSearchofovertime = DBSession.query(OidControlTime).filter(and_(OidControlTime.oid == oid, OidControlTime.Status == 1)).first()
            
            if getSearchofovertime:
                return dict(Status='Success', Overtime=getSearchofovertime.timeover)
                
            else:
                msg = 'MySQL could not found oid %s overtime in database.' % (oid)
                return dict(Status='False', msg=msg)

        except Exception, e:
            return dict(Status='False', msg=str(e))
    
    def addintozoneinformamt(self, gamename, gamePYname, zonename, zonePYname, Status):
        
        try:
            getSearchofzoneinformamt = DBSession.query(ZoneInformByAMT).filter(and_(ZoneInformByAMT.gamePYname == gamePYname, ZoneInformByAMT.zonePYname == zonePYname)).first()
            
            if getSearchofzoneinformamt:
                getSearchofzoneinformamt.gamename = gamename
                getSearchofzoneinformamt.zonename = zonename
                getSearchofzoneinformamt.Status = Status
            else:
                DBSession.add(ZoneInformByAMT(gamename, gamePYname, zonename, zonePYname, Status))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        return dict(Status='Success')
    
    def searchinmaintianlist(self, gamePYname, zonePYname):
        
        try:
            getSearchaboutmaintianlist = DBSession.query(ZoneInformByAMT).filter(and_(ZoneInformByAMT.gamePYname == gamePYname, ZoneInformByAMT.zonePYname == zonePYname)).first()
            if getSearchaboutmaintianlist:
                if getSearchaboutmaintianlist.Status == 0:
                    return dict(Status='Success', maintian='No')
                elif getSearchaboutmaintianlist.Status == 1:
                    return dict(Status='Success', maintian='Yes')
                elif getSearchaboutmaintianlist.Status == 500:
                    return dict(Status='Success', maintian='Unknown')
            else:
                return dict(Status='False', msg='MySQL could not found this zone.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
    
    def searchOIDexist(self, oid):
        
        try:
            getAlloid = DBSession.query(OidRequest).filter_by(OID=oid).first()
            
            if getAlloid:
                self.oidexist['Status'] = 'Success'
                self.oidexist['VariablesRequest'] = getAlloid.VariablesRequest
                self.oidexist['VariablesOut'] = getAlloid.VariablesOut
                self.oidexist['Nullable'] = getAlloid.Nullable
            else:
                self.oidexist['Status'] = 'False'
                self.oidexist['msg'] = 'MySQL could not found oid in table.oidrequest.'
            
        except Exception, e:
            return e   
        
        return self.oidexist
    
    def searchFieldType(self, field):
        
        try:
            getField = DBSession.query(OIDVariable).filter_by(variableName=field).first()
            
            if getField:
                self.fieldtype['Status'] = 'Success'
                self.fieldtype[getField.variableName] = dict(struct=getField.struct, dataType=getField.dataType, default=getField.default)

            else:
                self.fieldtype['Status'] = 'False'
                self.fieldtype['msg'] = 'MySQL could not found field : %s in table.oidvariable' % field
                
        except Exception, e:
            return e
        
        return self.fieldtype
    
    def searchFieldDefault(self, field):
        
        try:
            getDefault = DBSession.query(OIDVariable).filter_by(variableName=field).first()
            
            if getDefault:
                self.fieldefault['Status'] = 'Success'
                self.fieldefault['defaultVariable'] = getDefault.default
            else:
                self.fieldefault['Status'] = 'False'
                self.fieldefault['msg'] = 'MySQL could not found field : %s in table.oidvariable' % field
        except Exception, e:
            return e
        
        return self.fieldefault
    
    def searchGamelistAboutPYname(self, gameid):
        
        try:
            getPYname = DBSession.query(GameList).filter_by(GameID=gameid).first()
            
            if getPYname:
                self.PYname['Status'] = 'Success'
                self.PYname['Name'] = getPYname.Name
                self.PYname['FullName'] = getPYname.FullName
            else:
                self.PYname['Status'] = 'False'
                self.PYname['msg'] = 'MySQL could not found GameID && PYname in table.gamelist'
            
        except Exception, e:
            return e
    
        return self.PYname
    
    def searchOIDinTemplate(self, oid):
        
        try:
            getTemplateOid = DBSession.query(Template).filter_by(OID=oid).first()
            
            if getTemplateOid:
                self.templateDict['Status'] = 'Success'
                self.templateDict['oid'] = getTemplateOid.OID
            else:
                self.templateDict['Status'] = 'False'
                self.templateDict['msg'] = 'MySQL could not OID in table.template'
                
        except Exception, e:
            return e
        
        return self.templateDict
    
    def searchOIDdetailinTemplate(self, oid):
        
        try:
            getOIDdetail = DBSession.query(Template).filter_by(OID=oid).first()
            
            if getOIDdetail:
                self.templateOIDdetail['Status'] = 'Success'
                self.templateOIDdetail['OID'] = oid
                self.templateOIDdetail['TemplateType'] = getOIDdetail.TemplateType
                self.templateOIDdetail['TemplateName'] = getOIDdetail.TemplateName
            else:
                self.templateOIDdetail['Status'] = 'False'
                self.templateOIDdetail['msg'] = 'MySQL could not OID in table.template'
            
        except Exception, e:
            return e
        
        return self.templateOIDdetail
    
    def searchOIDdetail(self, oid):
        
        try:
            getTemplateOid = DBSession.query(EventRelation).filter_by(OID=oid).first()
            
            if getTemplateOid:
                self.oidDetail['Status'] = 'Success'
                self.oidDetail['eventType'] = getTemplateOid.eventType
                self.oidDetail['eventVar'] = getTemplateOid.eventVar
            else:
                self.oidDetail['Status'] = 'False'
                self.oidDetail['msg'] = 'MySQL could not OID in table.template'
                
        except Exception, e:
            return e
        
        return self.oidDetail
    
    ''' This method used to search gameID by gameName'''
    def searchGameIDbyGamename(self, gamename):
        
        try:
            getGameID = DBSession.query(GameList).filter_by(Name=gamename).first()
            
            if getGameID:
                self.Gid['Status'] = 'Success'
                self.Gid['GameID'] = getGameID.GameID
                self.Gid['GameFullName'] = getGameID.FullName
            else:
                self.Gid['Status'] = 'False'
                self.Gid['msg'] = 'MySQL could not Gamename in table.gamelist.'
            
        except Exception, e:
            return e
        
        return self.Gid
    
    ''' This method used to search FullName from GameList. '''
    def searchGameNamebyFullname(self, Fullname):
        
        try:
            getGameName = DBSession.query(GameList).filter_by(FullName = Fullname).first()
            
            if getGameName:
                tmpDict = {}
                if getGameName.IsUse != 1:
                    msg = 'Select Game : %s Unused.' % getGameName.Name
                    return dict(Status='False', msg=msg)
                else:
                    tmpDict['GameID'] = getGameName.GameID
                    tmpDict['Name'] = getGameName.Name
                    return dict(Status='Success', Return=tmpDict)
            else:
                getReturn = self.searchGameIDbyGamename('Unknown')
                return dict(Status='Warning', Return=dict(GameID=getReturn['GameID'], FullName=getReturn['FullName'], Name='Unknown'))
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
    
    ''' This method to get thresID '''
    def searchThresID(self, gameid, threstype):
        
        try:
            getThresID = DBSession.query(ThresRelation).filter(and_(ThresRelation.gameid == gameid, ThresRelation.thresType == threstype)).first()
            
            if getThresID:
                self.thresID['Status'] = 'Success'
                self.thresID['ThresNumberID'] = getThresID.ThresNumberID
            else:
                self.thresID['Status'] = 'False'
                self.thresID['msg'] = 'MySQL could not ThresNumberID in table.thresrelation'      
            
        except Exception, e:
            return e
        
        return self.thresID
    
    ''' This method to get thres Detail information '''
    def searchThresDetail(self, thresID):
        
        try:
            getDetail = DBSession.query(ThresNumber).filter_by(thresID = thresID).first()
            
            if getDetail:
                self.thresDetail['Status'] = 'Success'
                self.thresDetail['thresLevel'] = getDetail.thresLevel
                self.thresDetail['thresValueOne'] = getDetail.thresValueOne
                self.thresDetail['thresValueTwo'] = getDetail.thresValueTwo
            else:
                self.thresDetail['Status'] = 'False'
                self.thresDetail['msg'] = 'MySQL could not found detail in table.thresnumber'
            
        except Exception, e:
            return e
        
        return self.thresDetail
    
    ''' This method used to search detail of ignore eventtype '''
    def searchIgnore(self, eventtype, gameID):
        
        try:
            getIgnore = DBSession.query(CurvesIgnore).filter(and_(CurvesIgnore.Category == eventtype, CurvesIgnore.gameID == gameID)).first()
            
            if getIgnore:
                self.typeIgnore['Status'] = 'False'
            else:
                self.typeIgnore['Status'] = 'Success'
            
        except Exception, e:
            return e
        
        return self.typeIgnore
    
    ''' This method used to search in tempprocess in database and found detail '''
    def tempSearchintempprocess(self, ipaddress, process, timestamp):
        
        try:
            searchtmp = DBSession.query(TempProcess).filter(TempProcess.Ipaddress == ipaddress).all()
            
            if searchtmp:
                for eachline in searchtmp:
                    DBSession.delete(eachline)
                    
                DBSession.commit()
                DBSession.add(TempProcess(ipaddress, process, int(timestamp)))
            else:
                DBSession.add(TempProcess(ipaddress, process, int(timestamp)))
    
        except Exception, e:
            DBSession.rollback()
            DBSession.add(TempProcess(ipaddress, process, int(timestamp)))
        
        DBSession.commit()

        return dict(Status='Success')
    
    ''' This is method used to search in tempprocess '''
    def searchtempprocess(self, ipaddress):
        
        try:
            searchtmps = DBSession.query(TempProcess).filter_by(Ipaddress = ipaddress).first()
            
            if searchtmps:
                self.searchTempprocess['Status'] = 'Success'
                self.searchTempprocess['process'] = searchtmps.Process
            else:
                self.searchTempprocess['Status'] = 'False'
                self.searchTempprocess['msg'] = 'MySQL could not found in temp.table.tempprocess.'
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Return=self.searchTempprocess)
    
    ''' This method used to search in hostnametoprocess '''
    def searchhostnametoprocess(self, hostname):
        
        try:
            searchhostname = DBSession.query(HostnameToProcess).filter_by(Hostname = hostname).all()
            
            processlist = []
            
            if searchhostname:
                self.searchhostname['Status'] = 'Success'
                for each in searchhostname:
                    processlist.append(each.Process)
                    
                self.searchhostname['processlist'] = processlist
            else:
                self.searchhostname['Status'] = 'False'
                self.searchhostname['msg'] = 'MySQL could not found in table.hostnametoprocess'
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Return=self.searchhostname)
    
    def searchzonetohost(self, hostname):
        
        try:
            getSearchofzonetohost = DBSession.query(ZonetoHost).filter_by(Hostname=hostname).first()
            
            if getSearchofzonetohost:
                self.zonetohost['Status'] = 'Success'
                self.zonetohost['zoneID'] = getSearchofzonetohost.zoneID
            else:
                self.zonetohost['Status'] = 'False'
                self.zonetohost['msg'] = 'MySQL could not found zoneID in table.zonetohost.'
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return self.zonetohost
    
    def searchgamelisttoarea(self, zoneID):
        
        try:
            getSearchoflisttoarea = DBSession.query(GameListtoArea).filter_by(ZoneID = zoneID).first()
            
            if getSearchoflisttoarea:
                self.gamelisttoarea['Status'] = 'Success'
                self.gamelisttoarea['GameID'] = getSearchoflisttoarea.GameID
                
            else:
                self.gamelisttoarea['Status'] = 'False'
                self.gamelisttoarea['msg'] = 'MySQL could not found GameID in table.gamelisttoarea.'
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return self.gamelisttoarea
     
    def getGameNamebyGameID(self, GameID):
        
        try:
            getSearchofgamename = DBSession.query(GameList).filter_by(GameID=GameID).first()
            
            if getSearchofgamename:
                self.gameName['Status'] = 'Success'
                self.gameName['Name'] = getSearchofgamename.Name
            else:
                self.gameName['Status'] = 'False'
                self.gameName['msg'] = 'MySQL couldnot found GameName in table.GameList.'
            
        except Exception, e:
            return dict(Status='False', msg=str(e))   
        
        return self.gameName
    
    def addintoAlarm(self, eventApart, eventGrade, OID, Data, Destination, Status='Inuse'):
        
        try:
	
            print "###### add into alarm :", eventApart, eventGrade, OID, Data, Destination
	
            # ''' step 1. check data in table.eventalarm and update '''
	    getSearchoid = DBSession.query(EventAlarm).filter(and_(EventAlarm.OID == OID, EventAlarm.Destination == Destination)).first()
	    if getSearchoid:
		getSearchoid.data = Data
    
	    else:
	    # ''' step 2. if data is not exist. add new Data in table.'''
            	length = len(DBSession.query(EventAlarm).all())
            	DBSession.add(EventAlarm(int(length)+1, eventApart, eventGrade, OID, Data, Destination, Status))

            DBSession.commit()
            
        except Exception, e:
            DBSession.rollback()
            return e
        
class AlarmSearch:
    
    def __init__(self):
        
        self.searchOID = {}
        self.searchGame = {}
        self.projectRelation = {}
        self.suregroup = {}
        self.belong = {}
        self.user = {}
        self.userinform = {}
        self.gameCH = {}
        self.eventrelation = {}
        self.changeinfoname = {}
        
    def searchinAlarm(self, oid, status='Inuse'):
        
        try:
            searchResult = DBSession.query(EventAlarm).filter(and_(EventAlarm.OID==oid,EventAlarm.Status==status)).all()
            
            if searchResult:
                
                for eachLine in range(len(searchResult)):
                    self.searchOID['Status'] = 'Success'
                    self.searchOID[searchResult[eachLine].iD] = dict(eventApart=searchResult[eachLine].eventApart, eventGrade=searchResult[eachLine].eventGrade, Data=searchResult[eachLine].Data, Destination=searchResult[eachLine].Destination)
            else:
                self.searchOID['Status'] = 'False'
                self.searchOID['msg'] = 'MySQL could not OID in table.eventalarm'
                
            
        except Exception, e:
            return e
        
        return self.searchOID
    
    ''' Sure about database table.gamelist <<< gameName IsUse is 1 or 0 >>>'''
    def sureGameStatus(self, gameName):
     
        try:
            searchGameStatus = DBSession.query(GameList).filter_by(Name = gameName).first()
            
            if searchGameStatus:
                if searchGameStatus.IsUse == 1:
                    self.searchGame['Status'] = 'Success'
                    self.searchGame['GameID'] = searchGameStatus.GameID
                else:
                    self.searchGame['Status'] = 'False'
                    self.searchGame['msg'] = 'Project : %s is forbidden.' % searchGameStatus.FullName
                
            else:
                self.searchGame['Status'] = 'False'
                self.searchGame['msg'] = 'MySQLdb could not found search in table.gamelist.'
                
        except Exception, e:
            return e
           
        return self.searchGame
    
    ''' Sure about database table.projecttogroup exist. '''
    def sureProjectGroup(self, gameID):
        
        try:
            searchProjectGroup = DBSession.query(ProjecttoGroup).filter_by(gameID = gameID).first()
            
            if searchProjectGroup:
                self.projectRelation['Status'] = 'Success'
                self.projectRelation['groupID'] = searchProjectGroup.groupID
            else:
                self.projectRelation['Status'] = 'False'
                self.projectRelation['msg'] = 'MySQL could not found relation in table.projecttogroup.'
 
        except Exception, e:
            return e
        
        return self.projectRelation
    
    ''' Sure about database table.alarmgroup exist.'''
    def sureGroupExist(self, groupID):
        
        try:
            searchGroupExist = DBSession.query(AlarmGroup).filter_by(groupID = groupID).first()
            
            if searchGroupExist:
                if searchGroupExist.groupStatus == 1:
                    self.suregroup['Status'] = 'Success'
                else:
                    self.suregroup['Status'] = 'False'
                    self.suregroup['msg'] = 'groupID : %s is forbidden.' % (groupID)
            else:
                self.suregroup['Status'] = 'False'
                self.suregroup['msg'] = 'MySQL could not found informaton in table.alarmgroup.'
                
        except Exception, e:
            return e
        
        return self.suregroup
    
    ''' Sure group which is always for broadcast '''
    def Broadcast(self, groupBelong=-1):
       
        tmpList = []
        
        try:
            searchBelong = DBSession.query(AlarmGroup).filter_by(groupBelong = groupBelong).all()
            
            if searchBelong:
                for eachgroup in range(len(searchBelong)):
                    if searchBelong[eachgroup].groupStatus == 1:
                        self.belong['Status'] = 'Success'
                        tmpList.append(searchBelong[eachgroup].groupID)
                
            else:
                self.belong['Status'] = 'False'
                self.belong['msg'] = 'MySQL could not found any broadcast group in table.alarmgroup.'

            if len(tmpList) != 0:
                self.belong['BroadCastList'] = tmpList

        except Exception, e:
            return e
        
        return self.belong
    
    ''' getUser from table.alarmrelation '''
    def getRelationofUser(self, groupID):
        
        tmpDict = {}
        
        try:
            searchRecord = DBSession.query(AlarmRelation).filter_by(gid=groupID).all()
            
            if searchRecord:
                self.user['Status'] = 'Success'
                for eachUser in range(len(searchRecord)):
                    self.user[searchRecord[eachUser].uid] = searchRecord[eachUser].ulevel
            
            else:
                self.user['Status'] = 'False'
                self.user['msg'] = 'MySQL could not found groupID relation in table.gid.'
            
        except Exception, e:
            return e
        
        return self.user
    
    ''' Sure user information and reback '''
    def SureUserInformation(self, userID):
        
        try:
            searchInform = DBSession.query(AlarmUser).filter_by(userID=userID).first()
            
            if searchInform:
                if searchInform.userStatus == 1:
                    self.userinform['Status'] = 'Success'
                    self.userinform['userName'] = searchInform.userName
                    self.userinform['OC'] = searchInform.OC
                    self.userinform['SMCD'] = searchInform.SMCD
                    self.userinform['MAIL'] = searchInform.MAIL
                else:
                    self.userinform['Status'] = 'False'
                    self.userinform['msg'] = 'UserID : %s user is forbidden.' % userID 
            else:
                self.userinform['Status'] = 'False'
                self.userinform['msg'] = 'MySQL could not found user information in table.alarmuser.'

        except Exception, e:
            return e
        
        return self.userinform
    
    ''' from gameName to get GameName Chinese '''
    def getgameNameCH(self, gameName):
        
        try:
            searchChinese = DBSession.query(GameList).filter_by(Name = gameName).first()
            
            if searchChinese:
                self.gameCH['Status'] = 'Success'
                self.gameCH['FullName'] = searchChinese.FullName    
            else:
                self.gameCH['Status'] = 'False'
                self.gameCH['msg'] = 'MySQL could not found gameChineseName in table.gamelist.'
                            
        except Exception, e:
            return e
        
        return self.gameCH

    def geteventgraderelation(self, eventgrade):
        
        try:
            getRelations = DBSession.query(EventGradeRelation).filter_by(grade = eventgrade).first()
            
            if getRelations:
                self.eventrelation['Status'] = 'Success'
                self.eventrelation['oc'] = getRelations.oc
                self.eventrelation['mail'] = getRelations.mail
                self.eventrelation['smcd'] = getRelations.smcd
            else:
                self.eventrelation['Status'] = 'False'
                self.eventrelation['msg'] = 'MySQL could not found eventgrade in table.eventgraderelation.'
            
        except Exception, e:
            return e
        
        return self.eventrelation
    
    ''' This part will be change name by Named '''
    def getInfoCheckGameName(self, infoName):
        
        try:
            getChangeinfoname = DBSession.query(InfoCheckGameName).filter_by(infoName = infoName).first()
            
            if getChangeinfoname:
                self.changeinfoname['Status'] = 'Success'
                self.changeinfoname['realName'] = getChangeinfoname.realName
#            else:
#                self.changeinfoname['Status'] = 'False'
#                self.changeinfoname['msg'] = 'MySQL could not found infoName in table.infocheckgamename.'
            
        except Exception, e:
            return e
        
        return self.changeinfoname
    
class CircultSearch:
    
    def __init__(self):
        
        self.addinto = {}
    
    def addCircult(self, gameID, eventGrade, data, timestamp, TakeoverPerson='None', Status=0, SustainableTime=48, carepeoplecount=0, Oid='None'):

        try:
            print "###### data:", data, type(data)
            ''' first change data input '''
            if type(data).__name__ == 'dict':
                data = str(data)
                data = base64Data().encode64(data)
            elif type(data).__name__ == 'list':
                data = changeList().listtostr(data)
                data = base64Data().encode64(data['String'])
            else:
                data = base64Data().encode64(data)
            
            ''' Judge same information '''
            getSame = DBSession.query(EventAlarm).filter(and_(EventAlarm.GameID == gameID, EventAlarm.Timestamp == timestamp)).first()
            if getSame:
                return dict(Status='Success')
            else:
                ''' add into eventalarm about event detail '''
#                getSearchofevent = DBSession.query(EventAlarm).all()
#                if len(getSearchofevent) == 0:
#                    newEid = int(len(getSearchofevent) + 1)
#                else:
#                    newEid = int(getSearchofevent[-1].EiD + 1)
                DBSession.add(EventAlarm(gameID, eventGrade, data, timestamp, Oid))
                DBSession.commit()
                
                getSearchofEid = DBSession.query(EventAlarm).filter(EventAlarm.Timestamp == timestamp, EventAlarm.Oid == Oid).first()
                newEid = getSearchofEid.EiD
            
                ''' add into eventcircultbasic '''
                getSearchofbasic = DBSession.query(EventCircultBasic).all()
                if len(getSearchofbasic) == 0:
                    newCid = int(len(getSearchofbasic) + 1)
                else:
                    newCid = int(getSearchofbasic[-1].Cid + 1)
                DBSession.add(EventCircultBasic(newCid, TakeoverPerson, Status, SustainableTime, carepeoplecount))
            
                ''' add into event circult relation '''
                getSearchofeventrelation = DBSession.query(EventCircuitRelation).all()
                if len(getSearchofeventrelation) == 0:
                    newRid = int(len(getSearchofeventrelation) + 1)
                else:
                    newRid = int(getSearchofeventrelation[-1].rid +1)
                DBSession.add(EventCircuitRelation(newRid, newEid, newCid))
                
                DBSession.commit()
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))   
        
        finally:
            DBSession.rollback()

        DBSession.commit()
        return dict(Status='Success')
    
    def curvesstore(self, message, timestamp):
        
        try:
            getSearchofstore = DBSession.query(CurvesOfpeopleStore).first()
            
            if getSearchofstore:
                getSearchofstore.message = message
                getSearchofstore.timestamp = timestamp
                
            else:
                DBSession.add(CurvesOfpeopleStore(message, timestamp))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))   
        
        DBSession.commit()
        return dict(Status='Success')
    
class EventTransportSearch:
    
    def __init__(self):
        
        self.getbasicstatus = {}
        self.gamelistall = {}
        self.eventlevel = {}
        self.sureeventlevel = {}
        self.eventAll = {}
        self.userall = {}
        self.gamegroupall = {}
        self.userexist = {}
        self.eventop = {}
        self.eventattitude = {}
        self.cidsearch = {}
        self.userinform = {}
        self.transport = {}
        self.intodatabase = {}
        self.restoreresult = {}
        self.recently = {}
        self.userevent = {}
        self.eventlist = {}
        self.stepbystep = {}
        self.resultbyresult = {}
        self.deleteevent = {}
        self.assetuserforall = {}
        self.cidfromeid = {}
        self.addcare = {}
        self.searchtemplateID = {}
        self.gidfortemplateid = {}
        self.groupdetail = {}
        self.userinformationbygid = {}
        self.changeNowevent = {}
    
    ''' This method use to select all line in table.eventcircultstatus then return.'''    
    def searchofbasicstatus(self):
        
        tmpDict = {}
        
        try:
            getBasicResult = DBSession.query(EventCircultStatus).all()
            
            if getBasicResult:
                self.getbasicstatus['Status'] = 'Success'
                for eachline in getBasicResult:
                    tmpDict[eachline.StatusID] = eachline.StatusDesc
                self.getbasicstatus['basicstatus'] = tmpDict
            else:
                self.getbasicstatus['Status'] = 'False'
                self.getbasicstatus['msg'] = 'MySQL could not found in table.eventcircultstatus.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.getbasicstatus
    
    ''' This method used to search gamelist in table.GameList. '''
    def searchGameListAll(self, isUse):
        
        try:
            getGameList = DBSession.query(GameList).filter_by(IsUse = isUse).all()
            
            if getGameList:
                self.gamelistall['Status'] = 'Success'
                for eachline in getGameList:
                    tmpDict = {}
                    tmpDict['Name'] = eachline.Name
                    tmpDict['FullName'] = eachline.FullName
                    self.gamelistall[eachline.GameID] = tmpDict
            else:
                self.gamelistall['Status'] = 'False'
                self.gamelistall['msg'] = 'MySQL could not found any result in table.GameList where IsUse = %s' % isUse
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.gamelistall
    
    ''' This method used to search event level '''
    def searcheventlevel(self):
        
        tmplevel = {}
        
        try:
            getSearchofeventlevel = DBSession.query(EventLevel).all()
            
            if getSearchofeventlevel:
                self.eventlevel['Status'] = 'Success'
                for eachline in getSearchofeventlevel:
                    tmplevel[eachline.eventLevelID] = eachline.levelExplain
                self.eventlevel['eventlevel'] = tmplevel
            else:
                self.eventlevel['Status'] = 'False'
                self.eventlevel['msg'] = 'MySQL could not found data in table.eventlevel.'
                
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.eventlevel
    
    ''' This method use to search event level is correct.'''
    def searcheventlevelexist(self, grade):
        
        try:
            getResultofeventlevel = DBSession.query(EventLevel).filter_by(eventLevelID = grade).first()
            
            if getResultofeventlevel:
                self.sureeventlevel['Status'] = 'Success'
            else:
                self.sureeventlevel['Status'] = 'False'
                self.sureeventlevel['msg'] = 'MySQL could not found grade in table.eventlevel.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.sureeventlevel
    
    ''' This method use to search event in table.eventalarm '''
    def searchEventTrue(self, GameID, eventLevel):
        
        try:
            getEvent = DBSession.query(EventAlarm).filter(and_(EventAlarm.GameID == GameID, EventAlarm.eventGrade == eventLevel)).all()
            
            if getEvent:
                self.eventAll['Status'] = 'Success'
                for eachline in getEvent:
                    self.eventAll[eachline.EiD] = dict(Data=eachline.Data, Timestamp=eachline.Timestamp)
            else:
                self.eventAll['Status'] = 'False'
                self.eventAll['msg'] = 'MySQL could not found any eventalarm information in table.eventalarm.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.eventAll
    
    ''' This method used to search user exist in table.alarmuser '''
    def searchUserExist(self, username):
        
        try:
            getUserexist = DBSession.query(AlarmUser).filter_by(userName = username).first()
            
            if getUserexist:
                self.userall['Status'] = 'Success'
            else:
                self.userall['Status'] = 'False'
                self.userall['msg'] = 'MySQL could not found user in table.alarmuser.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.userall
    
    ''' This method used to search GroupID by GameID in table.gamegrouprelation '''
    def searchGroupIDbyGameID(self, GameID):
        
        try:
            getGroupIDfromGameID = DBSession.query(GameGroupRelation).filter_by(GameID=GameID).first()
            
            if getGroupIDfromGameID:
                self.gamegroupall['Status'] = 'Success'
                self.gamegroupall['GroupID'] = getGroupIDfromGameID.GroupID 
            else:
                self.gamegroupall['Status'] = 'False'
                self.gamegroupall['msg'] = 'MySQL could not found groupID by GameID.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.gamegroupall
    
    ''' Sure User exist in table.alarmuser. '''
    def SureUserExist(self, username):
        
        try:
            getSureName = DBSession.query(AlarmUser).filter_by(userName=username).first()
            
            if getSureName:
                if getSureName.userStatus == 0:
                    self.userexist['Status'] = 'False'
                    self.userexist['msg'] = 'user : %s could not allowed.'
                else:
                    self.userexist['Status'] = 'Success'
            else:
                self.userexist['Status'] = 'False'
                self.userexist['msg'] = 'MySQL could not found user : %s in table.Alarmuser.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))

        return self.userexist
    
    ''' get event operation part see '''
    def searchEventOperation(self, Oid):
        
        try:
            getEventOp = DBSession.query(EventOperation).filter_by(Oid=Oid).first()
            
            if getEventOp:
                self.eventop['Status'] = 'Success'
                self.eventop['OName'] = getEventOp.OName
            else:
                self.eventop['Status'] = 'False'
                self.eventop['msg'] = 'MySQL could not found eventoperation in table.eventoperation.'
     
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.eventop
    
    ''' This method use to search event attitude. '''
    def searchEventAttitude(self, Eid, Sid):
        
        try:
            getsearchEventattitude = DBSession.query(EventCircuitRelation).filter_by(Eid = Eid).first()
            
            if getsearchEventattitude:
                getCid = getsearchEventattitude.Cid
                
                getSearchComfotable = self.searchCid(getCid, Sid)
                if getSearchComfotable['Status'] == 'Success':
                    self.eventattitude['Status'] = 'Success'
                else:
                    self.eventattitude['Status'] = 'False'
                    self.eventattitude['msg'] = 'EventID:%s could not comfotable.' % (Eid)
            else:
                self.eventattitude['Status'] = 'False'
                self.eventattitude['msg'] = 'MySQL could not found event attitude in table.eventcircultrelation.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.eventattitude
        
    ''' This method use to search cid in table.eventcircultbasic '''
    def searchCid(self, Cid, StatusID):
        
        try:
            getcidfromtable = DBSession.query(EventCircultBasic).filter(and_(EventCircultBasic.Cid == Cid, EventCircultBasic.Status == StatusID)).first()
            
            if getcidfromtable:
                self.cidsearch['Status'] = 'Success'
            else:
                self.cidsearch['Status'] = 'False'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.cidsearch
    
    ''' This is method used to search of any value. '''
    def searchUserforSelect(self):
        
        try:
            getuserinform = DBSession.query(AlarmUser).filter_by(userStatus = 1).all()
            
            if getuserinform:
                self.userinform['Status'] = 'Success'
                for eachline in getuserinform:
                    self.userinform[eachline.userID] = eachline.userName
            else:
                self.userinform['Status'] = 'False'
                self.userinform['msg'] = 'MySQL could not found data in table.alarmuser.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.userinform
    
    ''' This method used to seearch transport of eventdefine in table.eventtransportdefine. '''
    def searcheventtransport(self, nowStatus, nextStatus):
        
        try:
            getSearchoftransport = DBSession.query(EventTransportDefine).filter(and_(EventTransportDefine.Tid == nowStatus, EventTransportDefine.Tnext == nextStatus)).all()
            
            if getSearchoftransport:
                self.transport['Status'] = 'Success'
                tmpEqual = []
                tmpNext = []
                tmpRollback = []
                self.transport['sourceStatus'] = nextStatus
                getSearchofnewTransport = DBSession.query(EventTransportDefine).filter_by(Tid=nextStatus).all()
                for eachline in getSearchofnewTransport:
                    tmpEqual.append(eachline.Tequal)
                    tmpNext.append(eachline.Tnext)
                    tmpRollback.append(eachline.Trollback)
                    
                ''' delete same element '''
                tmpEqual = {}.fromkeys(tmpEqual).keys()
                tmpNext = {}.fromkeys(tmpNext).keys()
                tmpRollback = {}.fromkeys(tmpRollback).keys()
                    
                self.transport['completeStatus'] = dict(equal=tmpEqual, next=tmpNext, rollback=tmpRollback)
            else:
                self.transport['Status'] = 'False'
                self.transport['msg'] = 'MySQL could not found in table.eventtransportdefine.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.transport
    
    ''' This method use to add data into database table.eventrecord. '''
    def AddDataintoRecord(self, EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark='None', OccurTime=0, deleteornot=0):
        
        try:
            getSearchofRecord = DBSession.query(EventRecord).count()
            
            RecordID = int(getSearchofRecord) + 1
            
            if type(EventID).__name__ != 'int':
                EventID = int(EventID)
                
            if type(nowStatus).__name__ != 'int':
                nowStatus = int(nowStatus)
                
            if type(nextStatus).__name__ != 'int':
                nextStatus = int(nextStatus)
            
            if type(opPeople).__name__ != 'str':
                opPeople = str(opPeople)
                
            if type(opTimestamp).__name__ != 'int':
                opTimestamp = int(opTimestamp)
            
            if type(Remark).__name__ != 'str':
                Remark = str(Remark)
                Remark = base64Data().encode64(Remark)
            else:
                Remark = base64Data().encode64(Remark)
            
            if type(OccurTime).__name__ == 'NoneType':
                OccurTime = 0
            elif type(OccurTime).__name__ != 'int':
                OccurTime = int(OccurTime)
            
            if type(deleteornot).__name__ == 'NoneType':
                deleteornot = 0    
            elif type(deleteornot).__name__ != 'int':
                deleteornot = int(deleteornot)
            
            DBSession.add(EventRecord(RecordID, EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark, OccurTime, deleteornot))

        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        return dict(Status='Success')

    ''' This method use to add data into resultdata table.eventrestoreresult. '''
    def AddRestoreResult(self, EventID, WhoClose, OccurTime, CloseTime, DeleteorNot, Detail):
        
        try:
            getSearchofRestore = DBSession.query(EventRestoreResult).count()
            
            RestoreID = int(getSearchofRestore) + 1
            
            if type(EventID).__name__ != 'int':
                EventID = int(EventID)
                
            if type(WhoClose).__name__ != 'str':
                WhoClose = str(WhoClose)
            
            if type(OccurTime).__name__ == 'NoneType':
                OccurTime = 0    
            elif type(OccurTime).__name__ != 'int':
                OccurTime = int(OccurTime)
                
            if type(CloseTime).__name__ != 'int':
                CloseTime = int(CloseTime)
            
            if type(DeleteorNot).__name__ == 'NoneType':
                DeleteorNot = 0    
            elif type(DeleteorNot).__name__ != 'int':
                DeleteorNot = int(DeleteorNot)    
                
            if type(Detail).__name__ != 'str':
                Detail = str(Detail)
                Detail = base64Data().encode64(Detail)
            else:
                Detail = base64Data().encode64(Detail)
                
            DBSession.add(EventRestoreResult(RestoreID, EventID, WhoClose, OccurTime, CloseTime, DeleteorNot, Detail))

        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()   
        return dict(Status='Success')
    
    ''' This method used to search recently event by web. '''
    def searchRecentlyEventbyweb(self, startpoint, count):
        
        tmpDict = {}
        self.recently['Recently'] = []
        
        try:
            '''[<EventAlarm: EiD="11", GameID="27", eventGrade="5", Data="eydtYWlsJzoge3030=", Timestamp="1323421012">]'''
            getrecently = DBSession.query(EventAlarm).order_by(desc(EventAlarm.EiD)).all()

            if getrecently:
                self.recently['Status'] = 'Success'
                try:
                    if len(getrecently) <= count:
                        for eachline in getrecently:
                            ''' Temp Statement '''
                            tmpDict = {}
                            tmpCount = 0
                            tmpEventID = ""
                            tmpEventName = ""
                            tmpFullDetail = ""
                            tmpGameName = ""
                            tmpGrade = ""
                            tmpEventStatus = ""
                            tmpData = ""
                            tmpTakeoverperson = ""
                            tmpTimestamp = ""
                            tmpStimestamp = ""
                            tmpCarepeople = 0
                            tmpGid = 0
                            tmpTemplateID = 0
                            tmpTemplateType = 'None'
                            tmpTemplateName = 'None'
                            tmpGroupName = 'None'
                            tmpGroupCHName = 'None'
                            tmpGroupuser = []
                            
                            ''' Temp Event ID => tmpEventID'''
                            tmpEventID = eachline.EiD
                            
                            getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                            if getAttachmentrelation:
                                tmpCid = getAttachmentrelation.Cid
                                getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                ''' Event Status => tmpEventStatus'''
                                tmpEventStatus = getAttachmentinformation.Status
                                ''' Take over person => tmpTakeoverperson'''
                                tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                ''' Stimestamp => tmpStimestamp * second'''
                                tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                ''' Care people count => tmpCarepeople'''
                                tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                    tmpCarepeople = 0 
                            else:
                                tmpCount = 0 
                            
                            ''' ProjectName => tmpGameName'''
                            getTempName = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                            if getTempName['Status'] != 'Success':
                                tmpGameName = 'Unknown'
                            else:
                                tmpGameName = getTempName['FullName']
                                    
                            ''' Detail => tmpData '''
                            tmpData = base64Data().decode64(eachline.Data)
                            
                            ''' Htimestamp => tmpTimestamp '''
                            tmpTimestamp = TimeBasic().timeControl(eachline.Timestamp, 3)
                            
                            ''' EventName => tmpEventName '''
                            if type(tmpData).__name__ != 'dict':
                                tmpEventName = changeDict().strtodict(tmpData)
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                            else:
                                tmpEventName = tmpData
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                            
                            ''' Event Grade => tmpGrade '''
                            tmpGrade = eachline.eventGrade
                                
                            ''' Oid get more detail '''
                            if eachline.Oid != 'None':
                                getTemplateID = EventTransportSearch().searchTemplateIDbyOid(eachline.Oid)
                                if getTemplateID['Status'] == 'Success':
                                    tmpTemplateID = getTemplateID['TemplateID']
                                    tmpTemplateName = getTemplateID['TemplateName']
                                    tmpTemplateType = getTemplateID['TemplateType']
                                        
                                getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                if getGids['Status'] == 'Success':
                                    tmpGid = getGids['gid']
                                    
                                getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                if getGroupdetail['Status'] == 'Success':
                                    tmpGroupName = getGroupdetail['Name']
                                    tmpGroupCHName = getGroupdetail['Desc']
                                        
                                getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                if getuserdetail['Status'] == 'Success':
                                    tmpGroupuser = getuserdetail['userinform']    
                                elif getuserdetail['Status'] == 'False':
                                    tmpGroupuser = {}
    
                            tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                            self.recently['Recently'].append(tmpDict)
                
                    
                    elif len(getrecently) > count:
                        for eachnum in range(count):
                            tmpThispoint = int(startpoint + eachnum)
                            
                            if tmpThispoint < len(getrecently):
                        
                                ''' Temp Statement '''
                                tmpDict = {}
                                tmpCount = 0
                                tmpEventID = ""
                                tmpEventName = ""
                                tmpFullDetail = ""
                                tmpGameName = ""
                                tmpGrade = ""
                                tmpEventStatus = ""
                                tmpData = ""
                                tmpTakeoverperson = ""
                                tmpTimestamp = ""
                                tmpStimestamp = ""
                                tmpCarepeople = 0
                                tmpGid = 0
                                tmpTemplateID = 0
                                tmpTemplateType = 'None'
                                tmpTemplateName = 'None'
                                tmpGroupName = 'None'
                                tmpGroupCHName = 'None'
                                tmpGroupuser = []
                                    
                                ''' Temp Event ID => tmpEventID'''
                                tmpEventID = getrecently[tmpThispoint].EiD
                                    
                                getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                                if getAttachmentrelation:
                                    tmpCid = getAttachmentrelation.Cid
                                    getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                    ''' Event Status => tmpEventStatus'''
                                    tmpEventStatus = getAttachmentinformation.Status
                                    ''' Take over person => tmpTakeoverperson'''
                                    tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                    ''' Stimestamp => tmpStimestamp * second'''
                                    tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                    ''' Care people count => tmpCarepeople'''
                                    tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                    if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                        tmpCarepeople = 0 
                                else:
                                    tmpCount = 0 
                                    
                                ''' ProjectName => tmpGameName'''
                                getTempName = EventSearch().searchGamelistAboutPYname(getrecently[tmpThispoint].GameID)
                                if getTempName['Status'] != 'Success':
                                    tmpGameName = 'Unknown'
                                else:
                                    tmpGameName = getTempName['FullName']
                                ''' Detail => tmpData '''
                                tmpData = base64Data().decode64(getrecently[tmpThispoint].Data)
                                    
                                ''' Htimestamp => tmpTimestamp '''
                                tmpTimestamp = TimeBasic().timeControl(getrecently[tmpThispoint].Timestamp, 3)
                                    
                                ''' EventName => tmpEventName '''
                                if type(tmpData).__name__ != 'dict':
                                    tmpEventName = changeDict().strtodict(tmpData)
                                    if tmpEventName['oc'] != '':
                                        tmpFullDetail = tmpEventName['oc']
                                        tmpEventName = tmpEventName['oc'][0:61]
                                    elif tmpEventName['smcd'] != '':
                                        tmpFullDetail = tmpEventName['smcd']
                                        tmpEventName = tmpEventName['smcd'][0:61]
                                    else:
                                        tmpCount = 0
                                else:
                                    tmpEventName = tmpData
                                    if tmpEventName['oc'] != '':
                                        tmpFullDetail = tmpEventName['oc']
                                        tmpEventName = tmpEventName['oc'][0:61]
                                    elif tmpEventName['smcd'] != '':
                                        tmpFullDetail = tmpEventName['smcd']
                                        tmpEventName = tmpEventName['smcd'][0:61]
                                    else:
                                        tmpCount = 0
                                    
                                ''' Event Grade => tmpGrade '''
                                tmpGrade = getrecently[tmpThispoint].eventGrade
                                    
                                ''' Oid get more detail '''
                                if getrecently[tmpThispoint].Oid != 'None':
                                    getTemplateID = EventTransportSearch().searchTemplateIDbyOid(getrecently[tmpThispoint].Oid)
                                    if getTemplateID['Status'] == 'Success':
                                        tmpTemplateID = getTemplateID['TemplateID']
                                        tmpTemplateName = getTemplateID['TemplateName']
                                        tmpTemplateType = getTemplateID['TemplateType']
                                            
                                    getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                    if getGids['Status'] == 'Success':
                                        tmpGid = getGids['gid']
                                        
                                    getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                    if getGroupdetail['Status'] == 'Success':
                                        tmpGroupName = getGroupdetail['Name']
                                        tmpGroupCHName = getGroupdetail['Desc']
                                            
                                    getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                    if getuserdetail['Status'] == 'Success':
                                        tmpGroupuser = getuserdetail['userinform']    
                                    elif getuserdetail['Status'] == 'False':
                                        tmpGroupuser = {}
                                    
                                tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                                self.recently['Recently'].append(tmpDict)
                        
                except Exception, e:
                    return dict(Status='False', msg=str(e))

            else:
                self.recently['Status'] = 'False'
                self.recently['msg'] = 'MySQL could not found alarm data. '    
    
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))  
        
        return self.recently
          
    ''' This method used to search recently 10 events. '''    
    def searchRecentlyEvent(self, Order, location):
        
        tmpDict = {}
        self.recently['Recently'] = []
        
        if Order == 'All':
            
            try:
                '''[<EventAlarm: EiD="11", GameID="27", eventGrade="5", Data="eydtYWlsJzoge3030=", Timestamp="1323421012">]'''
                getrecently = DBSession.query(EventAlarm).order_by(desc(EventAlarm.EiD)).all()

                if getrecently:
                    self.recently['Status'] = 'Success'
                    if len(getrecently) <= 10:
                        for eachline in getrecently:
                            ''' Temp Statement '''
                            tmpDict = {}
                            tmpCount = 0
                            tmpEventID = ""
                            tmpEventName = ""
                            tmpFullDetail = ""
                            tmpGameName = ""
                            tmpGrade = ""
                            tmpEventStatus = ""
                            tmpData = ""
                            tmpTakeoverperson = ""
                            tmpTimestamp = ""
                            tmpStimestamp = ""
                            tmpCarepeople = 0
                            tmpGid = 0
                            tmpTemplateID = 0
                            tmpTemplateType = 'None'
                            tmpTemplateName = 'None'
                            tmpGroupName = 'None'
                            tmpGroupCHName = 'None'
                            tmpGroupuser = []
                        
                            ''' Temp Event ID => tmpEventID'''
                            tmpEventID = eachline.EiD
                        
                            getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                            if getAttachmentrelation:
                                tmpCid = getAttachmentrelation.Cid
                                getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                ''' Event Status => tmpEventStatus'''
                                tmpEventStatus = getAttachmentinformation.Status
                                ''' Take over person => tmpTakeoverperson'''
                                tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                ''' Stimestamp => tmpStimestamp * second'''
                                tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                ''' Care people count => tmpCarepeople'''
                                tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                    tmpCarepeople = 0 
                            else:
                                tmpCount = 0 
                        
                            ''' ProjectName => tmpGameName'''
                            getTempName = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                            if getTempName['Status'] != 'Success':
                                tmpGameName = 'Unknown'
                            else:
                                tmpGameName = getTempName['FullName']
                                
                            ''' Detail => tmpData '''
                            tmpData = base64Data().decode64(eachline.Data)
                        
                            ''' Htimestamp => tmpTimestamp '''
                            tmpTimestamp = TimeBasic().timeControl(eachline.Timestamp, 3)
                        
                            ''' EventName => tmpEventName '''
                            if type(tmpData).__name__ != 'dict':
                                tmpEventName = changeDict().strtodict(tmpData)
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                            else:
                                tmpEventName = tmpData
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                        
                            ''' Event Grade => tmpGrade '''
                            tmpGrade = eachline.eventGrade
                            
                            ''' Oid get more detail '''
                            if eachline.Oid != 'None':
                                getTemplateID = EventTransportSearch().searchTemplateIDbyOid(eachline.Oid)
                                if getTemplateID['Status'] == 'Success':
                                    tmpTemplateID = getTemplateID['TemplateID']
                                    tmpTemplateName = getTemplateID['TemplateName']
                                    tmpTemplateType = getTemplateID['TemplateType']
                                    
                                getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                if getGids['Status'] == 'Success':
                                    tmpGid = getGids['gid']
                                
                                getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                if getGroupdetail['Status'] == 'Success':
                                    tmpGroupName = getGroupdetail['Name']
                                    tmpGroupCHName = getGroupdetail['Desc']
                                    
                                getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                if getuserdetail['Status'] == 'Success':
                                    tmpGroupuser = getuserdetail['userinform']    

                            tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                            self.recently['Recently'].append(tmpDict)
                                   
                    elif len(getrecently) > 10:
                        for eachnum in range(10):
                            ''' Temp Statement '''
                            tmpDict = {}
                            tmpCount = 0
                            tmpEventID = ""
                            tmpEventName = ""
                            tmpFullDetail = ""
                            tmpGameName = ""
                            tmpGrade = ""
                            tmpEventStatus = ""
                            tmpData = ""
                            tmpTakeoverperson = ""
                            tmpTimestamp = ""
                            tmpStimestamp = ""
                            tmpCarepeople = 0
                            tmpGid = 0
                            tmpTemplateID = 0
                            tmpTemplateType = 'None'
                            tmpTemplateName = 'None'
                            tmpGroupName = 'None'
                            tmpGroupCHName = 'None'
                            tmpGroupuser = []
                            
                            ''' Temp Event ID => tmpEventID'''
                            tmpEventID = getrecently[eachnum].EiD
                            
                            getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                            if getAttachmentrelation:
                                tmpCid = getAttachmentrelation.Cid
                                getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                ''' Event Status => tmpEventStatus'''
                                tmpEventStatus = getAttachmentinformation.Status
                                ''' Take over person => tmpTakeoverperson'''
                                tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                ''' Stimestamp => tmpStimestamp * second'''
                                tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                ''' Care people count => tmpCarepeople'''
                                tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                    tmpCarepeople = 0 
                            else:
                                tmpCount = 0 
                            
                            ''' ProjectName => tmpGameName'''
                            getTempName = EventSearch().searchGamelistAboutPYname(getrecently[eachnum].GameID)
                            if getTempName['Status'] != 'Success':
                                tmpGameName = 'Unknown'
                            else:
                                tmpGameName = getTempName['FullName']
                            ''' Detail => tmpData '''
                            tmpData = base64Data().decode64(getrecently[eachnum].Data)
                            
                            ''' Htimestamp => tmpTimestamp '''
                            tmpTimestamp = TimeBasic().timeControl(getrecently[eachnum].Timestamp, 3)
                            
                            ''' EventName => tmpEventName '''
                            if type(tmpData).__name__ != 'dict':
                                tmpEventName = changeDict().strtodict(tmpData)
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                            else:
                                tmpEventName = tmpData
                                if tmpEventName['oc'] != '':
                                    tmpFullDetail = tmpEventName['oc']
                                    tmpEventName = tmpEventName['oc'][0:61]
                                elif tmpEventName['smcd'] != '':
                                    tmpFullDetail = tmpEventName['smcd']
                                    tmpEventName = tmpEventName['smcd'][0:61]
                                else:
                                    tmpCount = 0
                            
                            ''' Event Grade => tmpGrade '''
                            tmpGrade = getrecently[eachnum].eventGrade
                            
                            ''' Oid get more detail '''
                            if getrecently[eachnum].Oid != 'None':
                                getTemplateID = EventTransportSearch().searchTemplateIDbyOid(getrecently[eachnum].Oid)
                                if getTemplateID['Status'] == 'Success':
                                    tmpTemplateID = getTemplateID['TemplateID']
                                    tmpTemplateName = getTemplateID['TemplateName']
                                    tmpTemplateType = getTemplateID['TemplateType']
                                    
                                getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                if getGids['Status'] == 'Success':
                                    tmpGid = getGids['gid']
                                
                                getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                if getGroupdetail['Status'] == 'Success':
                                    tmpGroupName = getGroupdetail['Name']
                                    tmpGroupCHName = getGroupdetail['Desc']
                                    
                                getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                if getuserdetail['Status'] == 'Success':
                                    tmpGroupuser = getuserdetail['userinform']    
                            
                            tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                            self.recently['Recently'].append(tmpDict)

                else:
                    self.recently['Status'] = 'False'
                    self.recently['msg'] = 'MySQL could not found alarm data. '    
    
            except Exception, e:
                DBSession.rollback()
                return dict(Status='False', msg=str(e))
        
        elif Order == 'After':
            
            if type(location).__name__ == 'NoneType' or location == 'None' or location == '':
                msg = 'select input ERROR: location:%s' % location
                return dict(Status='False', msg=msg)
            else:
                try:
                    getrecently = DBSession.query(EventAlarm).filter(EventAlarm.EiD > int(location)).all()
                    if getrecently:
                        self.recently['Status'] = 'Success'
                        for eachline in getrecently:
            
                            if len(getrecently) <= 10:
                                for eachline in getrecently:
                                    ''' Temp Statement '''
                                    tmpDict = {}
                                    tmpCount = 0
                                    tmpEventID = ""
                                    tmpEventName = ""
                                    tmpGameName = ""
                                    tmpGrade = ""
                                    tmpEventStatus = ""
                                    tmpData = ""
                                    tmpTakeoverperson = ""
                                    tmpTimestamp = ""
                                    tmpStimestamp = ""
                                    tmpCarepeople = ""
                                    tmpGid = 0
                                    tmpTemplateID = 0
                                    tmpTemplateType = 'None'
                                    tmpTemplateName = 'None'
                                    tmpGroupName = 'None'
                                    tmpGroupCHName = 'None'
                                    tmpGroupuser = []
                                
                                    ''' Temp Event ID => tmpEventID'''
                                    tmpEventID = eachline.EiD
                                    tmpCount += 1
                                
                                    getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                                    if getAttachmentrelation:
                                        tmpCid = getAttachmentrelation.Cid
                                        getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                        ''' Event Status => tmpEventStatus'''
                                        tmpEventStatus = getAttachmentinformation.Status
                                        tmpCount += 1
                                        ''' Take over person => tmpTakeoverperson'''
                                        tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                        tmpCount += 1
                                        ''' Stimestamp => tmpStimestamp * second'''
                                        tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                        tmpCount += 1
                                        ''' Care people count => tmpCarepeople'''
                                        tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                        tmpCount += 1
                                    else:
                                        tmpCount = 0 
                                
                                    ''' ProjectName => tmpGameName'''
                                    getTempName = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                                    if getTempName['Status'] != 'Success':
                                        tmpGameName = 'Unknown'
                                    else:
                                        tmpGameName = getTempName['FullName']
                                        tmpCount += 1
                                        
                                    ''' Detail => tmpData '''
                                    tmpData = base64Data().decode64(eachline.Data)
                                    tmpCount += 1
                                
                                    ''' Htimestamp => tmpTimestamp '''
                                    tmpTimestamp = TimeBasic().timeControl(eachline.Timestamp, 3)
                                    tmpCount += 1
                                
                                    ''' EventName => tmpEventName '''
                                    if type(tmpData).__name__ != 'dict':
                                        tmpEventName = changeDict().strtodict(tmpData)
                                        if tmpEventName['oc'] != '':
                                            tmpEventName = tmpEventName['oc'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        elif tmpEventName['smcd'] != '':
                                            tmpEventName = tmpEventName['smcd'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        else:
                                            tmpCount = 0
                                    else:
                                        tmpEventName = tmpData
                                        if tmpEventName['oc'] != '':
                                            tmpEventName = tmpEventName['oc'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        elif tmpEventName['smcd'] != '':
                                            tmpEventName = tmpEventName['smcd'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        else:
                                            tmpCount = 0
                                
                                    ''' Event Grade => tmpGrade '''
                                    tmpGrade = eachline.eventGrade
                                    tmpCount += 1
                                    
                                    ''' Oid get more detail '''
                                    if eachline.Oid != 'None':
                                        getTemplateID = EventTransportSearch().searchTemplateIDbyOid(eachline.Oid)
                                        if getTemplateID['Status'] == 'Success':
                                            tmpTemplateID = getTemplateID['TemplateID']
                                            tmpTemplateName = getTemplateID['TemplateName']
                                            tmpTemplateType = getTemplateID['TemplateType']
                                            
                                        getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                        if getGids['Status'] == 'Success':
                                            tmpGid = getGids['gid']
                                        
                                        getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                        if getGroupdetail['Status'] == 'Success':
                                            tmpGroupName = getGroupdetail['Name']
                                            tmpGroupCHName = getGroupdetail['Desc']
                                            
                                        getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                        if getuserdetail['Status'] == 'Success':
                                            tmpGroupuser = getuserdetail['userinform']
                                
                                    if tmpCount == 10:
                                        tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople)
                                        self.recently['Recently'].append(tmpDict)
                                    else:
                                        tmpDict = dict(EventID=tmpEventID, msg="output Value Error.")
                                        self.recently['Recently'].append(tmpDict)
                                           
                            elif len(getrecently) > 10:
                                for eachnum in range(10):
                                    ''' Temp Statement '''
                                    tmpDict = {}
                                    tmpCount = 0
                                    tmpEventID = ""
                                    tmpEventName = ""
                                    tmpGameName = ""
                                    tmpGrade = ""
                                    tmpEventStatus = ""
                                    tmpData = ""
                                    tmpTakeoverperson = ""
                                    tmpTimestamp = ""
                                    tmpStimestamp = ""
                                    tmpCarepeople = ""
                                    tmpGid = 0
                                    tmpTemplateID = 0
                                    tmpTemplateType = 'None'
                                    tmpTemplateName = 'None'
                                    tmpGroupName = 'None'
                                    tmpGroupCHName = 'None'
                                    tmpGroupuser = []
                                    
                                    ''' Temp Event ID => tmpEventID'''
                                    tmpEventID = getrecently[eachnum].EiD
                                    tmpCount += 1
                                    
                                    getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                                    if getAttachmentrelation:
                                        tmpCid = getAttachmentrelation.Cid
                                        getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                        ''' Event Status => tmpEventStatus'''
                                        tmpEventStatus = getAttachmentinformation.Status
                                        tmpCount += 1
                                        ''' Take over person => tmpTakeoverperson'''
                                        tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                        tmpCount += 1
                                        ''' Stimestamp => tmpStimestamp * second'''
                                        tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                        tmpCount += 1
                                        ''' Care people count => tmpCarepeople'''
                                        tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                        tmpCount += 1
                                    else:
                                        tmpCount = 0 
                                    
                                    ''' ProjectName => tmpGameName'''
                                    getTempName = EventSearch().searchGamelistAboutPYname(getrecently[eachnum].GameID)
                                    if getTempName['Status'] != 'Success':
                                        tmpGameName = 'Unknown'
                                    else:
                                        tmpGameName = getTempName['FullName']
                                        tmpCount += 1
                                    ''' Detail => tmpData '''
                                    tmpData = base64Data().decode64(getrecently[eachnum].Data)
                                    tmpCount += 1
                                    
                                    ''' Htimestamp => tmpTimestamp '''
                                    tmpTimestamp = TimeBasic().timeControl(getrecently[eachnum].Timestamp, 3)
                                    tmpCount += 1
                                    
                                    ''' EventName => tmpEventName '''
                                    if type(tmpData).__name__ != 'dict':
                                        tmpEventName = changeDict().strtodict(tmpData)
                                        if tmpEventName['oc'] != '':
                                            tmpEventName = tmpEventName['oc'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        elif tmpEventName['smcd'] != '':
                                            tmpEventName = tmpEventName['smcd'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        else:
                                            tmpCount = 0
                                    else:
                                        tmpEventName = tmpData
                                        if tmpEventName['oc'] != '':
                                            tmpEventName = tmpEventName['oc'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        elif tmpEventName['smcd'] != '':
                                            tmpEventName = tmpEventName['smcd'][0:61].decode('unicode-escape')
                                            tmpCount += 1
                                        else:
                                            tmpCount = 0
                                    
                                    ''' Event Grade => tmpGrade '''
                                    tmpGrade = getrecently[eachnum].eventGrade
                                    tmpCount += 1
                                    
                                    ''' Oid get more detail '''
                                    if getrecently[eachnum].Oid != 'None':
                                        getTemplateID = EventTransportSearch().searchTemplateIDbyOid(getrecently[eachnum].Oid)
                                        if getTemplateID['Status'] == 'Success':
                                            tmpTemplateID = getTemplateID['TemplateID']
                                            tmpTemplateName = getTemplateID['TemplateName']
                                            tmpTemplateType = getTemplateID['TemplateType']
                                            
                                        getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                        if getGids['Status'] == 'Success':
                                            tmpGid = getGids['gid']
                                        
                                        getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                        if getGroupdetail['Status'] == 'Success':
                                            tmpGroupName = getGroupdetail['Name']
                                            tmpGroupCHName = getGroupdetail['Desc']
                                            
                                        getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                        if getuserdetail['Status'] == 'Success':
                                            tmpGroupuser = getuserdetail['userinform']
                                    
                                    if tmpCount == 10:
                                        tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople)
                                        self.recently['Recently'].append(tmpDict)
                                    else:
                                        tmpDict = dict(EventID=tmpEventID, msg="output Value Error.")
                                        self.recently['Recently'].append(tmpDict)
                        else:
                            self.recently['Status'] = 'False'
                            self.recently['msg'] = 'MySQL could not found alarm data. '    
    
                except Exception, e:
                    DBSession.rollback()
                    return dict(Status='False', msg=str(e))        
                
        elif Order == 'Before':
            
            if type(location).__name__ == 'NoneType' or location == 'None' or location == '':
                msg = 'select input ERROR: location:%s' % location
                return dict(Status='False', msg=msg)
            else:
                try:                
                    getrecently = DBSession.query(EventAlarm).filter(EventAlarm.EiD < int(location)).all()
                    getcount = len(getrecently)

                    if getrecently:
                        self.recently['Status'] = 'Success'
            
                        if len(getrecently) <= 10:
                            for eachline in getrecently:
                                ''' Temp Statement '''
                                tmpDict = {}
                                tmpCount = 0
                                tmpEventID = ""
                                tmpEventName = ""
                                tmpFullDetail = ""
                                tmpGameName = ""
                                tmpGrade = ""
                                tmpEventStatus = ""
                                tmpData = ""
                                tmpTakeoverperson = ""
                                tmpTimestamp = ""
                                tmpStimestamp = ""
                                tmpCarepeople = 0
                                tmpGid = 0
                                tmpTemplateID = 0
                                tmpTemplateType = 'None'
                                tmpTemplateName = 'None'
                                tmpGroupName = 'None'
                                tmpGroupCHName = 'None'
                                tmpGroupuser = []
                                
                                ''' Temp Event ID => tmpEventID'''
                                tmpEventID = eachline.EiD
                                
                                getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                                if getAttachmentrelation:
                                    tmpCid = getAttachmentrelation.Cid
                                    getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                    ''' Event Status => tmpEventStatus'''
                                    tmpEventStatus = getAttachmentinformation.Status
                                    ''' Take over person => tmpTakeoverperson'''
                                    tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                    ''' Stimestamp => tmpStimestamp * second'''
                                    tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                    ''' Care people count => tmpCarepeople'''
                                    tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                    if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                        tmpCarepeople = 0 
                                else:
                                    tmpCount = 0 
                                
                                ''' ProjectName => tmpGameName'''
                                getTempName = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                                if getTempName['Status'] != 'Success':
                                    tmpGameName = 'Unknown'
                                else:
                                    tmpGameName = getTempName['FullName']
                                        
                                ''' Detail => tmpData '''
                                tmpData = base64Data().decode64(eachline.Data)
                                
                                ''' Htimestamp => tmpTimestamp '''
                                tmpTimestamp = TimeBasic().timeControl(eachline.Timestamp, 3)
                                
                                ''' EventName => tmpEventName '''
                                if type(tmpData).__name__ != 'dict':
                                    tmpEventName = changeDict().strtodict(tmpData)
                                    if tmpEventName['oc'] != '':
                                        tmpFullDetail = tmpEventName['oc']
                                        tmpEventName = tmpEventName['oc'][0:61]
                                    elif tmpEventName['smcd'] != '':
                                        tmpFullDetail = tmpEventName['smcd']
                                        tmpEventName = tmpEventName['smcd'][0:61]
                                    else:
                                        tmpCount = 0
                                else:
                                    tmpEventName = tmpData
                                    if tmpEventName['oc'] != '':
                                        tmpFullDetail = tmpEventName['oc']
                                        tmpEventName = tmpEventName['oc'][0:61]
                                    elif tmpEventName['smcd'] != '':
                                        tmpFullDetail = tmpEventName['smcd']
                                        tmpEventName = tmpEventName['smcd'][0:61]
                                    else:
                                        tmpCount = 0
                                
                                ''' Event Grade => tmpGrade '''
                                tmpGrade = eachline.eventGrade
                                
                                ''' Oid get more detail '''
                                if eachline.Oid != 'None':
                                    getTemplateID = EventTransportSearch().searchTemplateIDbyOid(eachline.Oid)
                                    if getTemplateID['Status'] == 'Success':
                                        tmpTemplateID = getTemplateID['TemplateID']
                                        tmpTemplateName = getTemplateID['TemplateName']
                                        tmpTemplateType = getTemplateID['TemplateType']
                                            
                                    getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                    if getGids['Status'] == 'Success':
                                        tmpGid = getGids['gid']
                                        
                                    getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                    if getGroupdetail['Status'] == 'Success':
                                        tmpGroupName = getGroupdetail['Name']
                                        tmpGroupCHName = getGroupdetail['Desc']
                                            
                                    getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                    if getuserdetail['Status'] == 'Success':
                                        tmpGroupuser = getuserdetail['userinform']
                                
                                tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                                self.recently['Recently'].append(tmpDict)

                                           
                        elif len(getrecently) > 10:
                                for eachnum in range(10):
                                    nowNumber = int(int(getcount) - (int(eachnum)+1))
                                    
                                    ''' Temp Statement '''
                                    tmpDict = {}
                                    tmpCount = 0
                                    tmpEventID = ""
                                    tmpEventName = ""
                                    tmpFullDetail = ""
                                    tmpGameName = ""
                                    tmpGrade = ""
                                    tmpEventStatus = ""
                                    tmpData = ""
                                    tmpTakeoverperson = ""
                                    tmpTimestamp = ""
                                    tmpStimestamp = ""
                                    tmpCarepeople = 0
                                    tmpGid = 0
                                    tmpTemplateID = 0
                                    tmpTemplateType = 'None'
                                    tmpTemplateName = 'None'
                                    tmpGroupName = 'None'
                                    tmpGroupCHName = 'None'
                                    tmpGroupuser = []
                                        
                                    ''' Temp Event ID => tmpEventID'''
                                    tmpEventID = getrecently[nowNumber].EiD
                                        
                                    getAttachmentrelation = DBSession.query(EventCircuitRelation).filter_by(Eid = tmpEventID).first()
                                    if getAttachmentrelation:
                                        tmpCid = getAttachmentrelation.Cid
                                        getAttachmentinformation = DBSession.query(EventCircultBasic).filter_by(Cid = tmpCid).first()
                                        ''' Event Status => tmpEventStatus'''
                                        tmpEventStatus = getAttachmentinformation.Status
                                        ''' Take over person => tmpTakeoverperson'''
                                        tmpTakeoverperson = getAttachmentinformation.TakeoverPerson
                                        ''' Stimestamp => tmpStimestamp * second'''
                                        tmpStimestamp = int(int(getAttachmentinformation.SustainableTime) * 60 * 60)
                                        ''' Care people count => tmpCarepeople'''
                                        tmpCarepeople = int(getAttachmentinformation.CarePeopleCount)
                                        if type(tmpCarepeople).__name__ == 'NoneType' or tmpCarepeople == '':
                                            tmpCarepeople = 0 
                                    else:
                                        tmpCount = 0 
                                        
                                    ''' ProjectName => tmpGameName'''
                                    getTempName = EventSearch().searchGamelistAboutPYname(getrecently[nowNumber].GameID)
                                    if getTempName['Status'] != 'Success':
                                        tmpGameName = 'Unknown'
                                    else:
                                        tmpGameName = getTempName['FullName']
                                    ''' Detail => tmpData '''
                                    tmpData = base64Data().decode64(getrecently[nowNumber].Data)
                                        
                                    ''' Htimestamp => tmpTimestamp '''
                                    tmpTimestamp = TimeBasic().timeControl(getrecently[nowNumber].Timestamp, 3)
                                        
                                    ''' EventName => tmpEventName '''
                                    if type(tmpData).__name__ != 'dict':
                                        tmpEventName = changeDict().strtodict(tmpData)
                                        if tmpEventName['oc'] != '':
                                            tmpFullDetail = tmpEventName['oc']
                                            tmpEventName = tmpEventName['oc'][0:61]
                                        elif tmpEventName['smcd'] != '':
                                            tmpFullDetail = tmpEventName['smcd']
                                            tmpEventName = tmpEventName['smcd'][0:61]
                                        else:
                                            tmpCount = 0
                                    else:
                                        tmpEventName = tmpData
                                        if tmpEventName['oc'] != '':
                                            tmpFullDetail = tmpEventName['oc']
                                            tmpEventName = tmpEventName['oc'][0:61]
                                        elif tmpEventName['smcd'] != '':
                                            tmpFullDetail = tmpEventName['smcd']
                                            tmpEventName = tmpEventName['smcd'][0:61]
                                        else:
                                            tmpCount = 0
                                        
                                    ''' Event Grade => tmpGrade '''
                                    tmpGrade = getrecently[nowNumber].eventGrade
                                    
                                    ''' Oid get more detail '''
                                    if getrecently[eachnum].Oid != 'None':
                                        getTemplateID = EventTransportSearch().searchTemplateIDbyOid(getrecently[eachnum].Oid)
                                        if getTemplateID['Status'] == 'Success':
                                            tmpTemplateID = getTemplateID['TemplateID']
                                            tmpTemplateName = getTemplateID['TemplateName']
                                            tmpTemplateType = getTemplateID['TemplateType']
                                            
                                        getGids = EventTransportSearch().searchGidfromtemplateID(tmpTemplateID)
                                        if getGids['Status'] == 'Success':
                                            tmpGid = getGids['gid']
                                        
                                        getGroupdetail = EventTransportSearch().searchgroupdetailbygid(tmpGid)
                                        if getGroupdetail['Status'] == 'Success':
                                            tmpGroupName = getGroupdetail['Name']
                                            tmpGroupCHName = getGroupdetail['Desc']
                                            
                                        getuserdetail = EventTransportSearch().searchuserinformation(tmpGid)
                                        if getuserdetail['Status'] == 'Success':
                                            tmpGroupuser = getuserdetail['userinform']
                                        
                                    tmpDict = dict(TemplateName=tmpTemplateName, TemplateType=tmpTemplateType, GroupName=tmpGroupName, GroupCHName=tmpGroupCHName, groupuser=tmpGroupuser, EventID=tmpEventID, EventName=tmpEventName, ProjectName=tmpGameName, EventGrade=tmpGrade, EventStatus=tmpEventStatus, Detail=tmpData, TakeoverPerson=tmpTakeoverperson, Htimestamp=tmpTimestamp, STimestamp=tmpStimestamp, CarePeopleCount=tmpCarepeople, FullDetail=tmpFullDetail)
                                    self.recently['Recently'].append(tmpDict)
                    else:
                        self.recently['Status'] = 'False'
                        self.recently['msg'] = 'MySQL could not found alarm data. '    
    
                except Exception, e:
                    DBSession.rollback()
                    return dict(Status='False', msg=str(e))

        return self.recently

    ''' This method use to add design to people into databse '''
    def addDesginintotable(self, EventID, opTimestamp, FromUser, ToUser, NowStatus='0', NextStatus='1', Remark='None'):
        
        try:
            ''' Step 1. check Variable '''
            if type(opTimestamp).__name__ == 'NoneType':
                opTimestamp = 0
            elif len(str(opTimestamp)) > 10:
                return dict(Status='False', msg='input opTimestamp ERROR. length')
            elif type(opTimestamp).__name__ != 'int':
                opTimestamp = int(opTimestamp)
            else:
                opTimestamp = opTimestamp
            
            if type(FromUser).__name__ == 'NoneType':
                return dict(Status='False', msg='input FromUser ERROR. Not None.')
            elif FromUser == '' or FromUser == 'None':
                FromUser = 'None'
            
            if type(ToUser).__name__ == 'NoneType':
                return dict(Status='False', msg='input ToUser ERROR. Not None.')
            elif ToUser == '' or ToUser == 'None':
                return dict(Status='False', msg='input ToUser ERROR. Not None.')
            
            if type(NowStatus).__name__ == 'NoneType':
                NowStatus = 0
            elif type(NowStatus).__name__ != 'str':
                NowStatus = int(NowStatus)
            
            if type(NextStatus).__name__ == 'NoneType':
                NextStatus = 0
            elif type(NextStatus).__name__ != 'str':
                NextStatus = int(NextStatus)
            
            if type(Remark).__name__ == 'NoneType':
                Remark = 'No Remark information.'
                Remark = base64Data().encode64(Remark)
            elif Remark == '' or Remark == 'None':
                Remark = 'No Remark information.'
                Remark = base64Data().encode64(Remark)
            else:
                Remark = base64Data().encode64(Remark)
            
            ''' Step 2. add into table. '''
            DBSession.add(DesigntoOther(EventID, FromUser, ToUser, opTimestamp, NowStatus, Remark))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        return dict(Status='Success')
    
    ''' This method use to search user's event in table.designtoother '''
    def searchUserevent(self, username):
        
        tmpDictEvent = {}
        tmpResourceData = ''
        
        try:
            getSearchofuserevent = DBSession.query(DesigntoOther).filter_by(ToUser = username).all()
            
            if getSearchofuserevent:
                self.userevent['Status'] = 'Success'
                for eachline in getSearchofuserevent:
                    ''' basic from designtoother '''
                    tmpEventID = eachline.EventID
                    tmpFromUser = eachline.FromUser
                    tmpTimestamp = TimeBasic().timeControl(eachline.opTimestamp, 3)
                    tmpRemark = base64Data().decode64(eachline.Remark)
                    
                    ''' get event resource data '''
                    tmpData = DBSession.query(EventAlarmDoing).filter_by(Eid=tmpEventID).first()
                    if tmpData:
                        tmpOccurTime = tmpData.OccurTime
                        tmpResourceData = base64Data().decode64(tmpData.Data)
                        tmpGame = EventSearch().searchGamelistAboutPYname(tmpData.GameID)
                        if tmpGame['Status'] != 'Success':
                            tmpGamePYname = 'None'
                        else:
                            tmpGamePYname = tmpGame['FullName']
                        tmpeventGrade = tmpData.eventGrade
                        tmpEventName = base64Data().decode64(tmpData.EventName)
                        tmpNowStatus = tmpData.NowStatus
                        tmpDatabaseData = base64Data().decode64(tmpData.Data)
                        tmpDatabaseData = changeDict().strtodict(tmpDatabaseData)
                        if tmpDatabaseData['oc'] != '':
                            tmpDatabaseData = tmpDatabaseData['oc']
                        elif tmpDatabaseData['smcd'] != '':
                            tmpDatabaseData = tmpDatabaseData['smcd']
                            
                        tmpDictEvent[tmpEventID] = dict(FullDetail = tmpDatabaseData, OccurTime=tmpOccurTime, GameName=tmpGamePYname, eventGrade=tmpeventGrade, EventName=tmpEventName, FromUser=tmpFromUser, opTimestamp=tmpTimestamp, Remark=tmpRemark, Data=tmpResourceData, NowStatus=tmpNowStatus)
                    else:
                        self.userevent['Status'] = 'False'
                        self.userevent['msg'] = 'MySQL could not found Resource Data in Table.'

                self.userevent['Allevent'] = tmpDictEvent
            else:
                self.userevent['Status'] = 'Success'
                self.userevent['msg'] = 'MySQL could not found any event belongs to user : %s' % (username)
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.userevent
    
    ''' This method used to get EventID list '''
    def searchEventIDlist(self, GameID, EventGrade):
        
        tmpList = []
        
        try:
            getSearchofEventIDlist = DBSession.query(EventAlarm).filter(and_(EventAlarm.GameID == GameID, EventAlarm.eventGrade == EventGrade)).all()
            
            if getSearchofEventIDlist:
                self.eventlist['Status'] = 'Success'
                for eachline in getSearchofEventIDlist:
                    tmpList.append(eachline.EiD)
                self.eventlist['EventID'] = tmpList
            else:
                self.eventlist['Status'] = 'False'
                self.eventlist['msg'] = 'MySQL could not found EventID in database.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.eventlist
    
    ''' This method used to search step by step '''
    def searchStepbyStep(self, EventID):
        
        tmpStepDict = {}
        
        try:
            getStepbyStep = DBSession.query(EventRecord).filter_by(EventID = EventID).all()
            print "##### getStepbyStep", getStepbyStep
            
            if getStepbyStep:
                self.stepbystep['Status'] = 'Success'
                for eachline in getStepbyStep:
                    tmpEventID = eachline.EventID
                    tmpPeople = eachline.opPeople
                    tmpTimestamp = TimeBasic().timeControl(eachline.opTimestamp, 3)
                    tmpRemark = base64Data().decode64(eachline.Remark)
                    tmpStepDict[tmpEventID] = dict(opPeople = tmpPeople, opTimestamp=tmpTimestamp, Remark=tmpRemark)
                self.stepbystep['step'] = tmpStepDict
            else:
                self.stepbystep['Status'] = 'False'
                self.stepbystep['msg'] = 'MySQL could not found any step in table.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.stepbystep
    
    ''' This method used to search result by result '''
    def searchresultbyresult(self, EventID):
        
        try:
            getresultbyeventID = DBSession.query(EventRestoreResult).filter_by(EventID=EventID).first()
            
            if getresultbyeventID:
                self.resultbyresult['Status'] = 'Success'
                tmpPeople = getresultbyeventID.WhoClose
                tmpOccurTime = TimeBasic().timeControl(getresultbyeventID.OccurTime, 3)
                tmpCloseTime = TimeBasic().timeControl(getresultbyeventID.CloseTime, 3)
                tmpDeleteorNot = getresultbyeventID.DeleteorNot
                tmpDetail = base64Data().decode64(getresultbyeventID.Detail)
                self.resultbyresult['result'] = dict(WhoClose=tmpPeople, OccurTime=tmpOccurTime, CloseTime=tmpCloseTime, DeleteorNot=tmpDeleteorNot, Detail=tmpDetail)
            else:
                self.resultbyresult['Status'] = 'False'
                self.resultbyresult['msg'] = 'MySQL could not found result in table.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.resultbyresult
    
    ''' This method used to delete event '''
    def deleteEvent(self, EventID):
        
        count = 0
        cid = ""
        
        try:
            ''' Part A. delete EventAlarm Eid '''
            getEventdelete = DBSession.query(EventAlarm).filter_by(EiD = EventID).first()
            
            if getEventdelete:
                DBSession.delete(getEventdelete)
                count += 1
            else:
                self.deleteevent['Status'] = 'False'
                self.deleteevent['msg'] = 'MySQL could not found eventID in table.EventAlarm.'
                
            ''' Part B. delete eventcircuitrelation Eid '''
            getEventcircultrrelationdelete = DBSession.query(EventCircuitRelation).filter_by(Eid=EventID).first()
            
            if getEventcircultrrelationdelete:
                cid = getEventcircultrrelationdelete.Cid
                DBSession.delete(getEventcircultrrelationdelete)
                count += 1
            else:
                self.deleteevent['Status'] = 'False'
                self.deleteevent['msg'] = 'MySQL could not found eventID in table.eventcircuitrelation'   
            
            ''' Part C. delete eventcircultbasic Cid '''
            geteventcircultbasicdelete = DBSession.query(EventCircultBasic).filter_by(Cid = cid).first()
            
            if geteventcircultbasicdelete:
                DBSession.delete(geteventcircultbasicdelete)
                count += 1
            else:
                self.deleteevent['Status'] = 'False'
                self.deleteevent['msg'] = 'MySQL could not found Cid in table.eventcircultbasic.'
             
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        if count == 3:
            self.deleteevent['Status'] = 'Success'
        else:
            self.deleteevent['Status'] = 'False'
            self.deleteevent['msg'] = 'MySQL could not operation.'
            DBSession.rollback()
            
        DBSession.commit()
        return self.deleteevent
    
    def insertintoweblog(self, username, timestamp, tablename, status, data):
        
        try:
            getinsertofweblog = DBSession.query(WebLog).count()
            newNid = int(getinsertofweblog) + 1
            
            DBSession.add(WebLog(newNid, username, timestamp, tablename, data, status))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        
        return dict(Status='Success')  
    
    def searchinassets(self, ipaddress):
        
        try:
            if re.search(r'^192|^172', ipaddress):   
                getSearchofipaddress = DBSession.query(ASSET).filter_by(companyIp = ipaddress).first()
                if getSearchofipaddress:
                    self.assetuserforall['serialNum'] = getSearchofipaddress.serialNum
                    self.assetuserforall['hostname'] = getSearchofipaddress.hostname
                    self.assetuserforall['comanyIp'] = getSearchofipaddress.companyIp
                    self.assetuserforall['outIp'] = getSearchofipaddress.outIp
                    self.assetuserforall['storeIp'] = getSearchofipaddress.storeIp
                    self.assetuserforall['username'] = getSearchofipaddress.username
                    self.assetuserforall['zcbm'] = getSearchofipaddress.zcbm
                    self.assetuserforall['machineroom'] = getSearchofipaddress.machineRoom
                    self.assetuserforall['useNow'] = getSearchofipaddress.useNow
                    self.assetuserforall['conProject'] = getSearchofipaddress.conProject
                    self.assetuserforall['rackPosition'] = getSearchofipaddress.rackPosition
                    self.assetuserforall['usage'] = getSearchofipaddress.usage
                    return dict(Status='Success', Detail=self.assetuserforall)
                else:
                    return dict(Status='False', msg='Could not found ipaddress in maximo.')
                
            else:
                getSearchofipaddress = DBSession.query(ASSET).filter_by(outIp = ipaddress).first()
                if getSearchofipaddress:
                    self.assetuserforall['serialNum'] = getSearchofipaddress.serialNum
                    self.assetuserforall['hostname'] = getSearchofipaddress.hostname
                    self.assetuserforall['comanyIp'] = getSearchofipaddress.companyIp
                    self.assetuserforall['outIp'] = getSearchofipaddress.outIp
                    self.assetuserforall['storeIp'] = getSearchofipaddress.storeIp
                    self.assetuserforall['username'] = getSearchofipaddress.username
                    self.assetuserforall['zcbm'] = getSearchofipaddress.zcbm
                    self.assetuserforall['machineroom'] = getSearchofipaddress.machineRoom
                    self.assetuserforall['useNow'] = getSearchofipaddress.useNow
                    self.assetuserforall['conProject'] = getSearchofipaddress.conProject
                    self.assetuserforall['rackPosition'] = getSearchofipaddress.rackPosition
                    self.assetuserforall['usage'] = getSearchofipaddress.usage
                    return dict(Status='Success', Detail=self.assetuserforall)
                else:
                    getSearchofipaddresstwice = DBSession.query(ASSET).filter_by(storeIp = ipaddress).first()
                    if getSearchofipaddresstwice:
                        self.assetuserforall['serialNum'] = getSearchofipaddresstwice.serialNum
                        self.assetuserforall['hostname'] = getSearchofipaddresstwice.hostname
                        self.assetuserforall['comanyIp'] = getSearchofipaddresstwice.companyIp
                        self.assetuserforall['outIp'] = getSearchofipaddresstwice.outIp
                        self.assetuserforall['storeIp'] = getSearchofipaddresstwice.storeIp
                        self.assetuserforall['username'] = getSearchofipaddresstwice.username
                        self.assetuserforall['zcbm'] = getSearchofipaddresstwice.zcbm
                        self.assetuserforall['machineroom'] = getSearchofipaddresstwice.machineRoom
                        self.assetuserforall['useNow'] = getSearchofipaddresstwice.useNow
                        self.assetuserforall['conProject'] = getSearchofipaddress.conProject
                        self.assetuserforall['rackPosition'] = getSearchofipaddress.rackPosition
                        self.assetuserforall['usage'] = getSearchofipaddress.usage
                        return dict(Status='Success', Detail=self.assetuserforall)
                    else:
                        return dict(Status='False', msg='Could not found ipaddress in maximo.')
                
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
    ''' This method used to search eventid exist in table.eventalarm. '''
    def searcheventidexist(self, EventID):
        
        try:
            getsearchofeventexist = DBSession.query(EventAlarm).filter_by(EiD=EventID).first()
            
            if getsearchofeventexist:
                return dict(Status='Success')
            else:
                return dict(Status='False', msg='MySQL could not found event in table.eventalarm.')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
    ''' This method used to search Cid exist. '''
    def searchCidfromEid(self, EventID):
        
        try:
            getsearchofCid = DBSession.query(EventCircuitRelation).filter_by(Eid = EventID).first()
            
            if getsearchofCid:
                self.cidfromeid['Status'] = 'Success'
                self.cidfromeid['Cid'] = getsearchofCid.Cid
            else:
                self.cidfromeid['Status'] = 'False'
                self.cidfromeid['msg'] = 'MySQL could not found any Cid from table.eventcircultrelation'
        
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
        return self.cidfromeid

    ''' This method used to add Carecount in eventcircultbasic '''
    def addcarecountfromCid(self, Cid):
        
        try:
            getAddfromCid = DBSession.query(EventCircultBasic).filter_by(Cid=Cid).first()
            
            if getAddfromCid:
                self.addcare['Status'] = 'Success'
                getAddfromCid.CarePeopleCount += 1
            else:
                self.addcare['Status'] = 'False'
                self.addcare['msg'] = 'MySQL could not found Cid from table.eventcircultbasic'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
        DBSession.commit()
        return self.addcare
    
    ''' This method use to template in template.'''
    def searchTemplateIDbyOid(self, Oid):
        
        try:
            getOid = DBSession.query(Template).filter_by(OID=Oid).first()
            
            if getOid:
                self.searchtemplateID['Status'] = 'Success'
                self.searchtemplateID['TemplateID'] = getOid.TemplateID
                self.searchtemplateID['TemplateName'] = getOid.TemplateName
                self.searchtemplateID['TemplateType'] = getOid.TemplateType
            else:
                self.searchtemplateID['Status'] = 'False'
                self.searchtemplateID['msg'] = 'MySQL could not found any templateID in table.template'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
        return self.searchtemplateID
    
    ''' This method used to search gid from templateID '''
    def searchGidfromtemplateID(self, TemplateID):
        
        try:
            getGidfromtemplate = DBSession.query(ResponibilityRelation).filter_by(TemplateID=TemplateID).first()
            
            if getGidfromtemplate:
                self.gidfortemplateid['Status'] = 'Success'
                self.gidfortemplateid['gid'] = getGidfromtemplate.gid
            else:
                self.gidfortemplateid['Status'] = 'False'
                self.gidfortemplateid['msg'] = 'MySQL could not found gid from templateID.'
                
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e)) 
        
        return self.gidfortemplateid
    
    ''' This method used to search responsible group detail '''
    def searchgroupdetailbygid(self, gid):
        
        try:
            getgroupdetail = DBSession.query(ResponibilityGroup).filter_by(gid=gid).first()
            
            if getgroupdetail:
                self.groupdetail['Status'] = 'Success'
                self.groupdetail['Name'] = getgroupdetail.Name
                self.groupdetail['Desc'] = getgroupdetail.Desc
            else:
                self.groupdetail['Status'] = 'False'
                self.groupdetail['msg'] = 'MySQL could not found any group information.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.groupdetail
    
    ''' This method used to search user information. '''
    def searchuserinformation(self, gid):
        
        tmpDict = {}
        
        try:
            getSearchofgid = DBSession.query(ResonibilityUser).filter_by(gid=gid).all()
            
            if getSearchofgid:
                self.userinformationbygid['Status'] = 'Success'
                for eachline in getSearchofgid:
                    tmpDict[eachline.uid] = dict(username=eachline.username, userPYname=eachline.userPYname, smcd=eachline.smcd, mail=eachline.mail, oc=eachline.oc, note=eachline.note, important=eachline.important)
                self.userinformationbygid['userinform'] = tmpDict    
            else:
                self.userinformationbygid['Status'] = 'False'
                self.userinformationbygid['msg'] = 'MySQL could not found any user.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.userinformationbygid
    
    ''' This part used to change event location from eventalarm to eventalarmdoing. '''
    def changeevent(self, Eventid, NowStatus, NextStatus, EventName, opTimestamp, OccurTime):
        
        if type(NowStatus) != 'int':
            NowStatus = int(NowStatus)
        else:
            NowStatus = NowStatus
            
        ''' 
        judge NowStatus is 0 or not. 
        if NowStatus != 0 : pass
        if NowStatus == 0 : continue
        '''    
        if NowStatus != 0:
            return dict(Status='Success')
                
        try:
            getSearchofeventid = DBSession.query(EventAlarm).filter_by(EiD=Eventid).first()
            
            if getSearchofeventid:
                self.changeNowevent['Status'] = 'Success'
                DBSession.add(EventAlarmDoing(getSearchofeventid.EiD, getSearchofeventid.GameID, getSearchofeventid.eventGrade, getSearchofeventid.Data, opTimestamp, OccurTime, getSearchofeventid.Oid, NextStatus, EventName))
                DBSession.delete(getSearchofeventid)
            else:
                self.changeNowevent['Status'] = 'False'
                self.changeNowevent['msg'] = 'MySQL could not found any event in eventalarm.'

        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        return self.changeNowevent
    
class EventTransportExpand(EventTransportSearch):
    
    def __init__(self):
        
        self.carepeople = {}
        self.addcarepeople = {}
        self.searchdoingbygameid = {}
        self.searchdoingbygrade = {}
        self.searchdoingbytwo = {}
        self.searchethinform = {}
        self.searchfromtableethinform = {}
        self.searchhid = {}
        self.searchproject = {}
        self.searcheventexist = {}
        self.searchdesigntoother = {}
        
    def searchcarepeople(self, Eid, Username):
        
        try:
            getSearchofcarepeople = DBSession.query(CarePeopleDetail).filter(and_(CarePeopleDetail.Eid == Eid, CarePeopleDetail.Username == Username)).first()
            
            if getSearchofcarepeople:
                self.carepeople['Status'] = 'False'
                self.carepeople['msg'] = 'Username:%s has attention Once.' % Username
            else:
                self.carepeople['Status'] = 'Success'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.carepeople
    
    def addcarepeopledetail(self, Eid, Username):
        
        try:
            getCount = DBSession.query(CarePeopleDetail).count()
            newCount = int(getCount + 1)
            DBSession.add(CarePeopleDetail(newCount, Eid, Username))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        self.addcarepeople['Status'] = 'Success'
        DBSession.commit()
        return self.addcarepeople
        
    def searcheventdoingbyGameID(self, GameID):
        
        tmpDict = []
        
        try:
            getSearchbygameID = DBSession.query(EventAlarmDoing).filter_by(GameID = GameID).all()
            
            if getSearchbygameID:
                self.searchdoingbygameid['Status'] = 'Success'
                for eachline in getSearchbygameID:
                    tmpEid = eachline.Eid
                    tmpGid = eachline.eventGrade
                    tmpData = base64Data().decode64(eachline.Data)
                    NewtmpData = changeDict().strtodict(tmpData)
                    tmpData = NewtmpData['smcd']
                    tmpOid = eachline.Oid
                    tmpEventname = base64Data().decode64(eachline.EventName)
                    tmpStatus = DataSearch().searcheachstatus(eachline.NowStatus)
                    if tmpStatus['Status'] == 'Success':
                        tmpdeStatus = tmpStatus['StatusDesc']
                    else:
                        tmpdeStatus = 'None'

                    getSearchofother = DBSession.query(EventRecord).filter(and_(EventRecord.EventID == tmpEid,EventRecord.nextStatus == eachline.NowStatus)).first()
                    if getSearchofother:
                        tmpopPeople = getSearchofother.opPeople
                        tmpopTimestamp = TimeBasic().timeControl(getSearchofother.opTimestamp, 3)
                        tmpOccurTime = TimeBasic().timeControl(getSearchofother.OccurTime, 3)
                        
                        tmpDict.append(dict(FullDetail=tmpData, EventID=tmpEid, EventGrade=tmpGid, Data=tmpData, EventName=tmpEventname, Oid=tmpOid, Status=tmpdeStatus, opPeople=tmpopPeople, opTimestamp=tmpopTimestamp, OccurTime=tmpOccurTime))
                    else:
                        self.searchdoingbygameid['Status'] = 'False'
                        self.searchdoingbygameid['msg'] = 'MySQL could not found any detail in other.'
            else:
                self.searchdoingbygameid['Status'] = 'False'
                self.searchdoingbygameid['msg'] = 'MySQL could not found any Gameinfo by gameID.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        self.searchdoingbygameid['Detail'] = tmpDict
        return self.searchdoingbygameid      
    
    def searchdetailbygrade(self, grade):
        
        tmpDict = []
        
        try:
            getSearchofgrade = DBSession.query(EventAlarmDoing).filter(EventAlarmDoing.eventGrade <= grade).all()
            
            if getSearchofgrade:
                self.searchdoingbygrade['Status'] = 'Success'
                for eachline in getSearchofgrade:
                    tmpEid = eachline.Eid
                    tmpGid = eachline.eventGrade
                    tmpData = base64Data().decode64(eachline.Data)
                    NewtmpData = changeDict().strtodict(tmpData)
                    tmpData = NewtmpData['smcd']
                    tmpOid = eachline.Oid
                    tmpEventname = base64Data().decode64(eachline.EventName)
                    tmpStatus = DataSearch().searcheachstatus(eachline.NowStatus)
                    if tmpStatus['Status'] == 'Success':
                        tmpdeStatus = tmpStatus['StatusDesc']
                    else:
                        tmpdeStatus = 'None'
                        
                    getSearchofother = DBSession.query(EventRecord).filter(and_(EventRecord.EventID == tmpEid,EventRecord.nextStatus == eachline.NowStatus)).first()
                    if getSearchofother:
                        tmpopPeople = getSearchofother.opPeople
                        tmpopTimestamp = TimeBasic().timeControl(getSearchofother.opTimestamp, 3)
                        tmpOccurTime = TimeBasic().timeControl(getSearchofother.OccurTime, 3)
                        
                        tmpDict.append(dict(FullDetail=tmpData, EventID=tmpEid, EventGrade=tmpGid, Data=tmpData, EventName=tmpEventname, Oid=tmpOid, Status=tmpdeStatus, opPeople=tmpopPeople, opTimestamp=tmpopTimestamp, OccurTime=tmpOccurTime))
                    else:
                        self.searchdoingbygrade['Status'] = 'False'
                        self.searchdoingbygrade['msg'] = 'MySQL could not found any grade comfortable'
            else:
                self.searchdoingbygrade['Status'] = 'False'
                self.searchdoingbygrade['msg'] = 'MySQL could not found any grade comfotable.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))  
        
        self.searchdoingbygrade['Detail'] = tmpDict
        return self.searchdoingbygrade
    
    def searchdetailbygameidandgrade(self, GameID, grade):
        
        tmpDict = []
        
        try:
            getsearchofbothgameidandgrade = DBSession.query(EventAlarmDoing).filter(EventAlarmDoing.GameID == GameID, EventAlarmDoing.eventGrade <= grade).all()
            
            if getsearchofbothgameidandgrade:
                self.searchdoingbytwo['Status'] = 'Success'
                for eachline in getsearchofbothgameidandgrade:
                    tmpEid = eachline.Eid
                    tmpGid = eachline.eventGrade
                    tmpData = base64Data().decode64(eachline.Data)
                    NewtmpData = changeDict().strtodict(tmpData)
                    tmpData = NewtmpData['smcd']
                    tmpOid = eachline.Oid
                    tmpEventname = base64Data().decode64(eachline.EventName)
                    tmpStatus = DataSearch().searcheachstatus(eachline.NowStatus)
                    if tmpStatus['Status'] == 'Success':
                        tmpdeStatus = tmpStatus['StatusDesc']
                    else:
                        tmpdeStatus = 'None'
                        
                    getSearchofother = DBSession.query(EventRecord).filter(and_(EventRecord.EventID == tmpEid,EventRecord.nextStatus == eachline.NowStatus)).first()
                    if getSearchofother:
                        tmpopPeople = getSearchofother.opPeople
                        tmpopTimestamp = TimeBasic().timeControl(getSearchofother.opTimestamp, 3)
                        tmpOccurTime = TimeBasic().timeControl(getSearchofother.OccurTime, 3)
                        
                        tmpDict.append(dict(FullDetail=tmpData, EventID=tmpEid, EventGrade=tmpGid, Data=tmpData, EventName=tmpEventname, Oid=tmpOid, Status=tmpdeStatus, opPeople=tmpopPeople, opTimestamp=tmpopTimestamp, OccurTime=tmpOccurTime))
                    else:
                        self.searchdoingbytwo['Status'] = 'False'
                        self.searchdoingbytwo['msg'] = 'MySQL could not found any detail in database.'
            else:
                self.searchdoingbytwo['Status'] = 'False'
                self.searchdoingbytwo['msg'] = 'MySQL could not found any detail in database.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        self.searchdoingbytwo['Detail'] = tmpDict
        return self.searchdoingbytwo
    
    def searchethdetailfromethdetail(self, ip):
        
        try:
            searchResult = DBSession.query(Ethdetail).filter_by(ip=ip).first()
            
            if searchResult:
                self.searchethinform['Status'] = 'Success'
                self.searchethinform['eid'] = searchResult.eid
                self.searchethinform['ethernet'] = searchResult.ethernet
            else:
                self.searchethinform['Status'] = 'False'
                self.searchethinform['msg'] = 'MySQL could not found any ip detail in database.'

        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.searchethinform
        
    def searchethinformfromethinform(self, column, eid):
        
        try:
            getSearchResult = DBSession.query(EthInfo).filter_by(Eth0 = eid).all()
            if getSearchResult:
                self.searchfromtableethinform['Status'] = 'Success'
                self.searchfromtableethinform['eid'] = getSearchResult[-1].eid
            else:
                getSearchTwice = DBSession.query(EthInfo).filter_by(Eth1 = eid).all()
                if getSearchTwice:
                    self.searchfromtableethinform['Status'] = 'Success'
                    self.searchfromtableethinform['eid'] = getSearchTwice[-1].eid
                else:
                    self.searchfromtableethinform['Status'] = 'False'
                    self.searchfromtableethinform['msg'] = 'MySQL could not found any detail in database.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))    
        
        return self.searchfromtableethinform
    
    def searchhidfromeid(self, eid):
        
        try:
            getSearchofHid = DBSession.query(AssetidtoEid).filter_by(eid=eid).first()
            
            if getSearchofHid:
                self.searchhid['Status'] = 'Success'
                self.searchhid['assetid'] = getSearchofHid.assetid
            else:
                self.searchhid['Status'] = 'False'
                self.searchhid['msg'] = 'MySQL could not found any hardward information.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.searchhid
    
    def searchProjectfromHid(self, hid):
        
        try:
            getSearchofProject = DBSession.query(AssetForAgent).filter_by(Hid=hid).first()
            
            if getSearchofProject:
                self.searchproject['Status'] = 'Success'
                self.searchproject['Project'] = getSearchofProject.ProjectName
                self.searchproject['HostName'] = getSearchofProject.HostName
                self.searchproject['ZCBM'] = getSearchofProject.ZCBM
            else:
                self.searchproject['Status'] = 'False'
                self.searchproject['msg'] = 'MySQL could not found project in database.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.searchproject
    
    def searcheventdoingexist(self, eventid):
        
        try:
            getSearchofEventidexist = DBSession.query(EventAlarmDoing).filter_by(Eid = eventid).first()
            
            if getSearchofEventidexist:
                self.searcheventexist['Status'] = 'Success'
                self.searcheventexist['opTime'] = getSearchofEventidexist.Timestamp
                self.searcheventexist['OccurTime'] = getSearchofEventidexist.OccurTime
                self.searcheventexist['GameID'] = getSearchofEventidexist.GameID
                self.searcheventexist['Data'] = getSearchofEventidexist.Data
                self.searcheventexist['Oid'] = getSearchofEventidexist.Oid
                self.searcheventexist['eventGrade'] = getSearchofEventidexist.eventGrade
                
            else:
                self.searcheventexist['Status'] = 'False'
                self.searcheventexist['msg'] = 'Event is not exist.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.searcheventexist
        
    def deleteeventdoingexist(self, eventid):
        
        try:
            getdoingexistdelete = DBSession.query(EventAlarmDoing).filter_by(Eid = eventid).first()
            
            if getdoingexistdelete:
                DBSession.delete(getdoingexistdelete)
                
                DBSession.commit()
                return dict(Status='Success')
            else:
                DBSession.commit()
                return dict(Status='Success')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
    
    def deletedesigntotherbyEventID(self, EventID):
        
        try:
            getSearchofdesigntootherEventID = DBSession.query(DesigntoOther).filter_by(EventID = EventID).first()
            
            if getSearchofdesigntootherEventID:
                DBSession.delete(getSearchofdesigntootherEventID)
                
                DBSession.commit()
                return dict(Status='Success')
            else:
                DBSession.commit()
                return dict(Status='Success')
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searcheventindesigntoother(self, eventid):
        
        try:
            getSearchofexistindesigntoother = DBSession.query(DesigntoOther).filter_by(EventID = eventid).first()
            
            if getSearchofexistindesigntoother:
                self.searchdesigntoother['Status'] = 'Success'
                self.searchdesigntoother['ToUser'] = getSearchofexistindesigntoother.ToUser
            else:
                self.searchdesigntoother['Status'] = 'False'
                self.searchdesigntoother['msg'] = 'MySQL could not found event in designtoother.'
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return self.searchdesigntoother
    
    def searchineventfinished(self, GameID, Username, opNum):
        
        tmpArray = []
        
        try:
            if opNum == 1:
                getSearch = DBSession.query(EventFinished).order_by(desc(EventFinished.CloseTime)).all()
                
                if getSearch:
                    for eachline in getSearch:
                        tmpDict = {}
                        tmpData = base64Data().decode64(eachline.Data)
                        tmpTime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        tmpOccurTime = TimeBasic().timeControl(eachline.OccurTime, 5) 
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        tmpPYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        if tmpPYname['Status'] != 'Success':
                            zhPYname = '未知游戏'
                        else:
                            zhPYname = tmpPYname['FullName']
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            oidPYname = '未知Oid匹配项'
                        else:
                            oidPYname = tmpOidPYname['TemplateName']
                            
                        tmpDict[eachline.Eid] = dict(DealTime = tmpDealTime, OccurTime = tmpOccurTime, Time = tmpTime, GameID = eachline.GameID, GamePYname = zhPYname, Data = tmpData, Oid = eachline.Oid, OidPYname = oidPYname, Detail = eachline.Detail, Username = eachline.Username)
                        tmpArray.append(tmpDict)
                else:
                    return dict(Status='False', msg='MySQL could not found any event in eventfinished.')
                
            elif opNum == 2:
                getSearch = DBSession.query(EventFinished).filter_by(GameID = GameID).order_by(desc(EventFinished.CloseTime)).all()
                
                if getSearch:
                    for eachline in getSearch:
                        tmpDict = {}
                        tmpData = base64Data().decode64(eachline.Data)
                        tmpPYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        tmpTime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        tmpOccurTime = TimeBasic().timeControl(eachline.OccurTime, 5) 
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        if tmpPYname['Status'] != 'Success':
                            zhPYname = '未知游戏'
                        else:
                            zhPYname = tmpPYname['FullName']
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            oidPYname = '未知Oid匹配项'
                        else:
                            oidPYname = tmpOidPYname['TemplateName']
                            
                        tmpDict[eachline.Eid] = dict(DealTime = tmpDealTime, OccurTime = tmpOccurTime, Time = tmpTime, GameID = eachline.GameID, GamePYname = zhPYname, Data = tmpData, Oid = eachline.Oid, OidPYname = oidPYname, Detail = eachline.Detail, Username = eachline.Username)
                        tmpArray.append(tmpDict)
                else:
                    return dict(Status='False', msg='MySQL could not found any event in eventfinished.')
                
            elif opNum == 3:
                
                getSearch = DBSession.query(EventFinished).filter_by(Username = Username).order_by(desc(EventFinished.CloseTime)).all()
                
                if getSearch:
                    for eachline in getSearch:
                        tmpDict = {}
                        tmpData = base64Data().decode64(eachline.Data)
                        tmpTime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        tmpPYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        tmpOccurTime = TimeBasic().timeControl(eachline.OccurTime, 5) 
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        if tmpPYname['Status'] != 'Success':
                            zhPYname = '未知游戏'
                        else:
                            zhPYname = tmpPYname['FullName']
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            oidPYname = '未知Oid匹配项'
                        else:
                            oidPYname = tmpOidPYname['TemplateName']
                            
                        tmpDict[eachline.Eid] = dict(DealTime = tmpDealTime, OccurTime = tmpOccurTime, Time = tmpTime, GameID = eachline.GameID, GamePYname = zhPYname, Data = tmpData, Oid = eachline.Oid, OidPYname = oidPYname, Detail = eachline.Detail, Username = eachline.Username)
                        tmpArray.append(tmpDict)
                else:
                    return dict(Status='False', msg='MySQL could not found any event in eventfinished.')
                
            elif opNum == 4:
                
                getSearch = DBSession.query(EventFinished).filter(and_(EventFinished.GameID == GameID, EventFinished.Username == Username)).order_by(desc(EventFinished.CloseTime)).all()
                
                if getSearch:
                    for eachline in getSearch:
                        tmpDict = {}
                        tmpData = base64Data().decode64(eachline.Data)
                        tmpTime = TimeBasic().timeControl(eachline.CloseTime, 5)
                        tmpPYname = EventSearch().searchGamelistAboutPYname(eachline.GameID)
                        tmpOccurTime = TimeBasic().timeControl(eachline.OccurTime, 5) 
                        tmpDealTime = TimeBasic().TimeMinus(eachline.OccurTime, eachline.CloseTime)
                        
                        if tmpPYname['Status'] != 'Success':
                            zhPYname = '未知游戏'
                        else:
                            zhPYname = tmpPYname['FullName']
                        tmpOidPYname = EventSearch().searchOIDdetailinTemplate(eachline.Oid)
                        if tmpOidPYname['Status'] != 'Success':
                            oidPYname = '未知Oid匹配项'
                        else:
                            oidPYname = tmpOidPYname['TemplateName']
                            
                        tmpDict[eachline.Eid] = dict(DealTime = tmpDealTime, OccurTime = tmpOccurTime, Time = tmpTime, GameID = eachline.GameID, GamePYname = zhPYname, Data = tmpData, Oid = eachline.Oid, OidPYname = oidPYname, Detail = eachline.Detail, Username = eachline.Username)
                        tmpArray.append(tmpDict)
                else:
                    return dict(Status='False', msg='MySQL could not found any event in eventfinished.')
        
            else:
                return dict(Status='False', msg='Operation Illegial.')
     
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success', Array=tmpArray)
    
    def addintoeventfinsied(self, Eid, GameID, Data, Oid, OccurTime=0, CloseTime=0, DeleteorNot=1, Detail='None', Username='None'):
        
        try:
            DBSession.add(EventFinished(Eid, GameID, Data, Oid, OccurTime, CloseTime, DeleteorNot, Detail, Username))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        DBSession.commit()
        
        return dict(Status='Success')
    
    def addintoMachineDown(self, zcbm, hostname, project, timestamp):
        
        try:
            getsearchofMachineDown = DBSession.query(ZCBM = zcbm).first()
            if getsearchofMachineDown: 
                getsearchofMachineDown.Timestamp = timestamp
            else:
                DBSession.add(MachineDown(zcbm, hostname, project, timestamp))
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success')
    
class SearchofEventSearch:
    
    def searchofeventdoing(self, startpoint, operation):

        try:
            from model.dbsearchExpand import Expand
            if operation == 'all':
                getSearchofallreturn = Expand().searchdoingeventofall()
                return getSearchofallreturn
            
            elif operation == 'After':
                getSearchofallreturn = Expand().searchdoingeventofafter(startpoint)
                return getSearchofallreturn
                
            elif operation == 'Before':
                getSearchofallreturn = Expand().searchdoingeventofbefore(startpoint)
                return getSearchofallreturn
                
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchofeventdoingWeb(self, startpoint, count):

        try:
            from model.dbsearchExpand import Expand

            getSearchofallreturn = Expand().searchdoingeventofallforweb(startpoint, count)
            return getSearchofallreturn

                
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchoffinishdoing(self, startpoint, operation):
        
        try:
            from model.dbsearchExpand import Expand
            if operation == 'all':
                getSearchofallreturn = Expand().searchfinisheddoingeventofall()
                return getSearchofallreturn
            
            elif operation == 'After':
                getSearchofallreturn = Expand().searchfinisheddoingeventofafter(startpoint)
                return getSearchofallreturn
                
            elif operation == 'Before':
                getSearchofallreturn = Expand().searchfinisheddoingeventofbefore(startpoint)
                return getSearchofallreturn
            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
    def searchoffinishdoingweb(self, startpoint, count):
        
        try:
            from model.dbsearchExpand import Expand

            getSearchofallreturn = Expand().searchfinisheddoingeventofallweb(startpoint, count)
            return getSearchofallreturn

            
        except Exception, e:
            DBSession.rollback()
            return dict(Status='False', msg=str(e))
        
