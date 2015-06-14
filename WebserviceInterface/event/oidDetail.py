# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from model import DBSession
from model.dbsearch import EventTransportExpand, EventSearch, CircultSearch
from model.physicalAsset import Ethdetail, EthInfo
from model.assetforagent import AssetForAgent, AssetidtoEid

from BaseClass.verifityDependence import changeDict
from BaseClass.timeBasic import TimeBasic
from ServiceConfig.config import readFromConfigFile
from interface.collection.dbconnect import Connect

from Depend import Dependence
from EventManager import Manager
from eventStep import EventProcessStep
from event.EventContent import eventContent
from event.Base.bodystruct import EventBody

class OidDetail:
    
    def __init__(self):
        
        self.returns = ""
        self.linkwithdatabase = {}
        
    def DetailforEachOid(self, name, message):
        
        # Oid = 1.1
        if name == 'insert':
            
            ''' Step 1. All information about input detail '''
            tmpProjectName = ""
            tmpProjectFunc = ""
            tmpKernel = ""
            tmpCpuCoreNum = ""
            tmpSerialNum = ""
            tmpZCBM = ""
            tmpMemory = ""
            tmpCpuType = ""
            tmpModel = ""
            tmpHostName = ""
            tmpOS = ""
            tmpManufacturer = ""
            tmpEthInfo = {}
            tmpTimestamp = int(round(time.time()))
            Resultofbody = {}
            
            for key,value in message.items():
                if key == 'Status':
                    if value != 'Success':
                        return dict(Status='False', msg='Message check Failed.')
            
            if type(message['Result']).__name__ == 'str':
                Resultofbody = changeDict().strtodict(message['Result'])
            else:
                Resultofbody = message['Result']
 
            for keys,values in Resultofbody.items():
                if keys == 'Project':
                    for K,V in Resultofbody[keys].items():
                        if K == 'Name':
                            tmpProjectName = self.changestr(V)
                        elif K == 'Func':
                            tmpProjectFunc = self.changestr(V)
                    
                elif keys == 'HwInfo':
                    for KK,VV in Resultofbody[keys].items():
                        if KK == 'Kernel':
                            tmpKernel = self.changestr(VV)
                        elif KK == 'CpuCoreNum':
                            tmpCpuCoreNum = self.changestr(VV)
                        elif KK == 'SN':
                            tmpSerialNum = self.changestr(VV)
                        elif KK == 'ZCBM':
                            tmpZCBM = self.changestr(VV)
                        elif KK == 'Memory':
                            tmpMemory = self.changestr(VV)
                        elif KK == 'CpuType':
                            tmpCpuType = self.changestr(VV)
                        elif KK == 'Model':
                            tmpModel = self.changestr(VV)
                        elif KK == 'HostName':
                            tmpHostName = self.changestr(VV)
                        elif KK == 'OS':
                            tmpOS = self.changestr(VV)
                        elif KK == 'Manufacturer':
                            tmpManufacturer = self.changestr(VV)
                            
                    
                elif keys == 'EthInfo':
                    
                    for eachline in Resultofbody[keys]:
                        tmpStatus = ''
                        tmpip = ''
                        tmpmask = ''
                        tmpethname = ''
                        for KKK, VVV in eachline.items():
                            if KKK == 'status':
                                tmpStatus = self.changestr(VVV)
                            elif KKK == 'ip':
                                tmpip = self.changestr(VVV)
                            elif KKK == 'mask':
                                tmpmask = self.changestr(VVV)
                            elif KKK == 'ethname':
                                tmpethname = self.changestr(VVV)
                                
                        tmpEthInfo[tmpethname] = dict(status=tmpStatus, ip=tmpip, mask=tmpmask)

            if tmpZCBM == '':
                return dict(Status='False', msg='Input Server has not ZCBM.')

            ''' get eth detail '''
            tmpEthDict = {}
            for key,value in tmpEthInfo.items():
                if key == 'eth0':
                    getSearchofeth = DBSession.query(Ethdetail).filter(Ethdetail.ip == value['ip'], Ethdetail.mask == value['mask']).first()
                    if getSearchofeth:
                        tmpEthDict['eth0'] = getSearchofeth.eid
                    else:
                        getethcount = DBSession.query(Ethdetail).count()
                        getethcount = (getethcount + 1)
                        DBSession.add(Ethdetail(getethcount,value['status'],value['ip'],value['mask'],'eth0'))
                        tmpEthDict['eth0'] = getethcount
                elif key == 'eth1':
                    getSearchofethone = DBSession.query(Ethdetail).filter(Ethdetail.ip == value['ip'], Ethdetail.mask == value['mask']).first()
                    if getSearchofethone:
                        tmpEthDict['eth1'] = getSearchofethone.eid
                    else:
                        getethcountone = DBSession.query(Ethdetail).count()
                        getethcountone = (getethcountone + 1)
                        DBSession.add(Ethdetail(getethcountone,value['status'],value['ip'],value['mask'],'eth1'))
                        tmpEthDict['eth1'] = getethcountone

            ''' Step 2. check server information exist. '''
            getSearchofHardware = DBSession.query(AssetForAgent).filter(AssetForAgent.ZCBM == tmpZCBM).first()
            if getSearchofHardware:
                try:
                    if int(getSearchofHardware.Timestamp) < message['SendTime']:

                        DBSession.delete(getSearchofHardware)
                        DBSession.commit()
                        
                        tmpeth0 = ""
                        tmpeth1 = ""
                        
                        for key,value in tmpEthDict.items():
                            if key == 'eth0':
                                tmpeth0 = value
                            elif key == 'eth1':
                                tmpeth1 = value
                        getCountofeth = DBSession.query(EthInfo).count()
                        getCountofeth = (getCountofeth + 1)
                        DBSession.add(EthInfo(getCountofeth,tmpeth0,tmpeth1,'None','None'))
                        
                        DBSession.add(AssetForAgent(tmpProjectName, tmpProjectFunc, tmpKernel, tmpCpuCoreNum, tmpSerialNum, tmpZCBM, tmpMemory, tmpCpuType, tmpModel, tmpHostName, tmpOS, tmpManufacturer, message['SendTime']))
                        DBSession.commit()
                        
                        getTmpid = DBSession.query(AssetForAgent).filter_by(ZCBM = tmpZCBM).first()
                        if getTmpid:
                            Tmpid = getTmpid.Hid
                        else:
                            DBSession.rollback()
                            return dict(Status='False', msg='flush assetforagent Error.')
                        
                        getCountofrelation = DBSession.query(AssetidtoEid).count()
                        getCountofrelation = int(getCountofrelation + 1)
                        DBSession.add(AssetidtoEid(getCountofrelation, Tmpid, getCountofeth))
                        
                        DBSession.commit()
                        return dict(Status='Success')
                        
                    else:
                        return dict(Status='Success', msg='Input Hostname Need not fresh.')
                    
                except Exception, e:
                    DBSession.commit()
                    return dict(Status='False', msg=str(e))
            else:
                try:
                    tmpHidforinsert = ""
                    
                    ''' insert into table'''
                    DBSession.add(AssetForAgent(tmpProjectName, tmpProjectFunc, tmpKernel, tmpCpuCoreNum, tmpSerialNum, tmpZCBM, tmpMemory, tmpCpuType, tmpModel, tmpHostName, tmpOS, tmpManufacturer, message['SendTime']))
                    DBSession.commit()
                    
                    getHid = DBSession.query(AssetForAgent).filter_by(ZCBM = tmpZCBM).first()
                    if getHid:
                        tmpHidforinsert = getHid.Hid
                    else:
                        DBSession.rollback()
                        return dict(Status='False', msg='insert into assetforagent error.')
                    
                    for key,value in tmpEthDict.items():
                        if key == 'eth0':
                            tmpeth0 = value
                        elif key == 'eth1':
                            tmpeth1 = value
                    getCountofeth = DBSession.query(EthInfo).count()
                    getCountofeth = (getCountofeth + 1)
                    DBSession.add(EthInfo(getCountofeth,tmpeth0,tmpeth1,'None','None'))
                    
                    getCountofrelation = DBSession.query(AssetidtoEid).count()
                    getCountofrelation = int(getCountofrelation + 1)
                    DBSession.add(AssetidtoEid(getCountofrelation, tmpHidforinsert, getCountofeth))
                
                except Exception, e:
                    DBSession.rollback()
                    return dict(Status='False', msg=str(e))
                
                DBSession.commit()
                return dict(Status='Success')
            
        # Oid = 1.2 
        elif name == 'disk':
            
            try:
                tablename = ""
                columnname = ""
                
                ''' Step 1. link with MainServer. '''
                getMainServerDict = readFromConfigFile().get_config_mainserver()
                for eachline in getMainServerDict['MainServer']:
                    if eachline[0] == 'username':
                        self.linkwithdatabase['username'] = eachline[1]
                    elif eachline[0] == 'port':
                        self.linkwithdatabase['port'] = int(eachline[1])
                    elif eachline[0] == 'ip':
                        self.linkwithdatabase['ipaddress'] = eachline[1]
                    elif eachline[0] == 'password':
                        self.linkwithdatabase['password'] = eachline[1]
                    elif eachline[0] == 'dbname':
                        self.linkwithdatabase['dbname'] = eachline[1]
                
                (ZConn, ZCursor) = Connect().createwithUtf8(self.linkwithdatabase)
                
                ''' Step 2. get Mainserver detail => ipaddress = tmpIP '''
                if message['Type'] == 'agent':
                    columnname = 'AgentID'
                    tablename = 'AgentList'
                elif message['Type'] == 'switch':
                    columnname = 'SwitchID'
                    tablename = 'SwitchList'
                elif message['Type'] == 'node':
                    columnname = 'NodeID'
                    tablename = 'NodeList'
                
                #pdb.set_trace()
                cmd = 'SELECT IP FROM %s where %s=%s' % (tablename, columnname, message['ID'])
                ZCursor.execute(cmd)
                result = ZCursor.fetchone()
                if type(result).__name__ != 'NoneType':
                    tmpIP = result[0]
                else:
                    msg = 'MySQL could not found any result in %s' % tablename
                    Connect().drop(ZConn, ZCursor)
                    return dict(Status='False', msg=msg)
                
                ''' Step 3. from ethdetail to get detail. '''
                getsearchinform = EventTransportExpand().searchethdetailfromethdetail(tmpIP)
                if getsearchinform['Status'] != 'Success':
                    Connect().drop(ZConn, ZCursor)
                    return getsearchinform
                else:
                    tmpEid = getsearchinform['eid']
                    tmpEthernet = getsearchinform['ethernet']
                    
                ''' Step 4. from ethinform get all eid. '''
                getsearchinformpart = EventTransportExpand().searchethinformfromethinform(tmpEthernet, tmpEid)
                if getsearchinformpart['Status'] != 'Success':
                    Connect().drop(ZConn, ZCursor)
                    return getsearchinformpart
                tmpWholeEid = getsearchinformpart['eid']
                
                ''' Step 5. from eid to get hid. '''
                getSearchofhid = EventTransportExpand().searchhidfromeid(tmpWholeEid)
                if getSearchofhid['Status'] != 'Success':
                    Connect().drop(ZConn, ZCursor)
                    return getSearchofhid
                tmpWholeHid = getSearchofhid['assetid']
                
                ''' Step 6. from Hid to get Project. '''
                getProject = EventTransportExpand().searchProjectfromHid(tmpWholeHid)
                if getProject['Status'] != 'Success':
                    Connect().drop(ZConn, ZCursor)
                    return getProject
                tmpProject = getProject['Project']
                tmpHostname = getProject['HostName']
                getGameID = EventSearch().searchGameIDbyGamename(tmpProject)
                if getGameID['Status'] != 'Success':
                    Connect().drop(ZConn, ZCursor)
                    return getGameID
                tmpGameID = getGameID['GameID']
                
                ''' Step 7. get ExceptionID from mainserver. '''
                cmd = 'SELECT ExceptionID FROM ExceptionLogic where OID=%s' % (message['OID'])
                ZCursor.execute(cmd)
                exresult = ZCursor.fetchall()
                if len(exresult) == 0:
                    Connect().drop(ZConn, ZCursor)
                    return dict(Status='False', msg='MySQL could not found exceptionID from database.')

                tmpExceptionList = []
                for eachlineofException in exresult:
                    tmpExceptionList.append(eachlineofException[0])
                
                tmpThresholdDict = {} 
                tmpDictforA = {}
                Dictforbody = {}  
                ''' Step 8. from threshold to get detail '''
                for eachlineExID in tmpExceptionList:
                    getcmd = 'SELECT EventLevel, ThresholdPercent from Threshold where GameID=%s and ExceptionID=%s' % (tmpGameID, eachlineExID)
                    ZCursor.execute(getcmd)
                    resultZ = ZCursor.fetchone()
                    if type(message['Result']).__name__ != 'dict':
                        Dictforbody = changeDict().strtodict(message['Result'])
                    else:
                        Dictforbody = message['Result']
  
                    for Keys,Values in Dictforbody.items():
                        Keys = self.changestr(Keys)
                        Values = self.changestr(Values)
                        dest = self.changestr(resultZ[1])
                        
                        newValues = int(Values[:-1])
                        newdest = int(dest[:-1])
                        if newValues > newdest:
                            tmpnewdata = "[%s]%s(%s) : '%s' (%s) over %s Level (%s) disk threshold." % (tmpProject, tmpHostname, str(tmpIP), Keys, Values, str(resultZ[0]), str(resultZ[1]))
                            mail = dict(subject='Disk Threshold', content=tmpnewdata)
                            data = dict(oc=tmpnewdata, smcd=tmpnewdata, mail=mail)
                            getInsertintoDatabase = CircultSearch().addCircult(tmpGameID, resultZ[0], data, message['SendTime'], 'None', 0, 48, 0, message['OID'])           
                            if getInsertintoDatabase['Status'] != 'Success':
                                Connect().drop(ZConn, ZCursor)
                                return getInsertintoDatabase
                    
                    
                ''' Step Finally: close connect '''
                Connect().drop(ZConn, ZCursor)

            except Exception, e:
                Connect().drop(ZConn, ZCursor)
                return dict(Status='False', msg=str(e))
        
            return dict(Status='Success')
        
        # Oid = 1.7    
        elif name == 'processInform':
            
            try:
                '''
                Step 1. insert into temp table tempprocess
                {'Status': 'Success', 
                 'Return': {
                             'Hostname': 'ZR-Agent-4-ZT2', 
                             'Ipaddress': '172.30.6.172', 
                             'MachineRoom': 'ZR'
                          }
                }
                '''
                getSearchMain = Manager().ManagerDecide(message, name)
                if getSearchMain['Status'] != 'Success':
                    return getSearchMain
                
                '''
                Step 2. judge event 
                example : {'Status': 'False', 'content': ['CharServer14']}
                          {'Status': 'Success'}
                '''
                getStepReturn = EventProcessStep().processStep(name, getSearchMain['Return']['Ipaddress'], message['SendTime'])
                if getStepReturn['Status'] != 'Success':
                    return getStepReturn
                
                ''' 
                Step 3. change content
                example : {'content': 'ZR-Agent-4.x-test \xe7\xbc\xba\xe5\xb0\x91\xe5\xa6\x82\xe4\xb8\x8b\xe8\xbf\x9b\xe7\xa8\x8b: CharServer14', 'Status': 'Success'}
                '''
                getContent = eventContent().changeContent(name, getSearchMain['Return']['Ipaddress'], getStepReturn['compare'])
                print "##### getContent:", getContent
                if getContent['Status'] != 'Success':
                    return getContent
                if re.search(r'None', getContent['content']):
                    return dict(Status='Success')
                
                '''
                Step 4. get basic information 
                A. judge >>> localhost <<< -> >>> localhost_ipaddress <<<
                B. get GameID
                C. change data struct
                '''
                
                # A. {'Status': 'Success', 'Name': 'ZT2'}
                #    {'Status': 'False', 'msg':''}
                getGameName = EventProcessStep().getGameID(getSearchMain['Return']['Ipaddress'])
                if getGameName['Status'] != 'Success':
                    return getGameName
                
                # B. {'Status': 'Success', 'hostname': 'ZR-Agent-4.x-test', 'ipaddress': '192.168.1.1'}
                #    {'Status': 'False', 'msg':''}
                JudgeHostname = EventProcessStep().HostnameJudge(name, getSearchMain['Return']['Hostname'], getSearchMain['Return']['Ipaddress'])
                if JudgeHostname['Status'] != 'Success':
                    return JudgeHostname
         
                '''
                Step 5. add into eventalarm
                '''
                addintodatabase = CircultSearch().addCircult(getGameName['GameID'], 5, getContent['content'], message['SendTime'], 'None', 0, 48, 0, '1.7')
                if addintodatabase['Status'] != 'Success':
                    return addintodatabase

            except Exception, e:
                return dict(Status='False', msg=str(e))
            
            return dict(Status='Success')
        
        # Oid = 5.1
        elif name == 'serveralive':
                        
            HidList = []
            
            '''
            {'Info': 'None', 
             'Status': 'Success', 
             'OID': '5.1', 
             'JobID': 0, 
             'Result': " {
                           u'57': u'disconn', 
                           u'377': u'disconn'
                         }", 
             'Type': 'main', 
             'ID': '0', 
             'SendTime': '1390893937'
            }
            '''
            # Step 1. check input
            getFirstcheck = Dependence().checkFirstdisconnbody(message)
            if getFirstcheck['Status'] != 'Success':
                return getFirstcheck
            
            # Step 2. get mainserver ip information
            # {'Status': 'Success', 'iplist': ['172.30.6.172']}
            getSecondfromMain = Manager().getfromMain(message)
            if getSecondfromMain['Status'] != 'Success':
                return getSecondfromMain
            
            # Step 3. from assetforagent to get detail => 
            for tmpIP in getSecondfromMain['iplist']:
                getsearchinform = EventTransportExpand().searchethdetailfromethdetail(tmpIP)
                if getsearchinform['Status'] != 'Success':
                    return getsearchinform
                else:
                    tmpEid = getsearchinform['eid']
                    tmpEthernet = getsearchinform['ethernet']
      
                getsearchinformpart = EventTransportExpand().searchethinformfromethinform(tmpEthernet, tmpEid)
                if getsearchinformpart['Status'] != 'Success':
                    return getsearchinformpart
                tmpWholeEid = getsearchinformpart['eid']
                
                getSearchofhid = EventTransportExpand().searchhidfromeid(tmpWholeEid)
                if getSearchofhid['Status'] != 'Success':
                    return getSearchofhid
                tmpWholeHid = getSearchofhid['assetid']
            
                HidList.append(tmpWholeHid)
                
            # Step 4. get hardware detail
            for eachHid in HidList:
                getDetail = EventTransportExpand().searchProjectfromHid(eachHid)
                if getDetail['Status'] == 'Success':
                    print "success"
            # ''' 等待敏杰梳理后面逻辑部分内容  '''
                
            
    def changestr(self, unicodestr):
        
        if type(unicodestr).__name__ == 'unicode':
            return unicodestr.encode('utf8')
        else:
            return unicodestr