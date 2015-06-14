# -*- coding: utf-8 -*-
''' @author : majian'''

''' SqlAlchemy Global Statement '''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# read from config -> setting.ini
from ServiceConfig.config import readFromConfigFile

user, passwd, ip, port, dbname = '','','','',''
Dict = readFromConfigFile().get_config_sqlalchemy('/WebserviceInterface/ServiceConfig/setting.ini')
for key,value in Dict.items():
    if key == 'database':
        for eachitem in range(len(value)):
            if value[eachitem][0] == 'username':
                user = value[eachitem][1]
            elif value[eachitem][0] == 'password':
                passwd = value[eachitem][1]
            elif value[eachitem][0] == 'port':
                port = value[eachitem][1]
            elif value[eachitem][0] == 'ip':
                ip = value[eachitem][1]
                
    elif key == 'interfaceDB':
        for eachitem in range(len(value)):
            if value[eachitem][0] == 'dbname':
                dbname = value[eachitem][1]

create_cmd = 'mysql://%s:%s@%s:%s/%s' % (user, passwd, ip, port, dbname)

engine = create_engine(create_cmd)

declarativeBase = declarative_base()
metadata = declarativeBase.metadata

maker = sessionmaker(bind=engine, autoflush=True, \
                         autocommit=False, expire_on_commit=False)

DBSession = scoped_session(maker)
DBSession.configure(bind=engine)


''' 
从这里导入和使用自己的表，在使用前会首先创建  
Part One : Interface Using Table
'''
from model.aduser import ADuser
from model.asset import ASSET
from model.curves import CURVES, CurvesIgnore
from model.translate import Translate
from model.gamename import Gameinform
from model.template import Template
from model.type import TypeVarify
from model.weblog import WebLog
from model.designate import DesigntoOther
from model.machinedown import MachineDown
from model.curvesofpeoplestore import CurvesOfpeopleStore
from model.carepeopledetail import CarePeopleDetail
from model.eventtransportdefine import EventTransportDefine
from model.Eventoperation import EventOperation
from model.eventAlarm import EventAlarm, EventLevel, EventAlarmDoing
from model.infocheckGamename import InfoCheckGameName
from model.zoneInform import ZonetoHost, ZoneInformByAMT
from model.assetforagent import AssetForAgent, AssetidtoEid
from model.alarmbasic import AlarmGroup, AlarmUser
from model.oidrepeat import OidRepeat, OidControlTime
from model.process import ProcessStandard, HostnameToProcess, TempProcess
from model.eventGraderelation import EventGradeRelation
from model.alarmRelation import AlarmRelation, ProjecttoGroup
from model.eventRelation import EventRelation, EventInterrlated
from model.thresNumber import ThresNumber, ThresRelation
from model.oidRelation import OidRequest, OIDVariable
from model.EventRecord import EventRecord, EventRestoreResult, EventFinished
from model.requestobject import AgentList, SwitchList, NodeList
from model.base import Packtype, Validate, Encrypt, Compress
from model.commandtype import CommandType, CommandTypeRelation
from model.responibility import ResonibilityUser, ResponibilityGroup, ResponibilityRelation
from model.gamelist import GameList, GameListtoArea, GameGroupRelation
from model.physicalAsset import AgenttoAssets, HosttoId, HardwareInfo, EthInfo, Ethdetail
from model.Eventcircuit import EventCircuitRelation, EventCircultBasic, EventCircultStatus
'''
Part Two : Website Using Table
'''
from model.website.processInfo import ProcessInfo
from model.website.systemAuthority import SystemAuthority
from model.website.systemRole import SystemRole
from model.website.systemUser import SystemUser
from model.website.systemRelation import SystemRelation


def init_model():
    ''' Call me before using any of the tables or classes in the model.'''

    try:
        metadata.create_all(engine)
        DBSession.commit()

    except:
        DBSession.rollback()
        raise
    
    finally:
        DBSession.commit()
        DBSession.close()   

        
