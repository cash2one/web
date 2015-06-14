# -*- coding: utf-8 -*-
''' @author : majian'''

''' SqlAlchemy Global Statement '''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# read from config -> setting.ini
from ServiceConfig.config import readFromConfigFile

user, passwd, ip, port, cmdbname = '','','','',''
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
                
    elif key == 'ConfigManagerDB':
        for eachitem in range(len(value)):
            if value[eachitem][0] == 'dbname':
                cmdbname = value[eachitem][1]

create_cmdb = 'mysql://%s:%s@%s:%s/%s' % (user, passwd, ip, port, cmdbname)
cmengine = create_engine(create_cmdb)

cmdeclarativeBase = declarative_base()

cmetadata = cmdeclarativeBase.metadata

cmmaker = sessionmaker(bind=cmengine, autoflush=True, \
                         autocommit=False, expire_on_commit=False)

CMDBSession = scoped_session(cmmaker)
CMDBSession.configure(bind=cmengine)

''' 
从这里导入和使用自己的表，在使用前会首先创建  
Part : Interface Using Table
'''
from model.Practicalusing.SplicingURL import SpliceURL
from model.Practicalusing.unifiedDnsIp import UnifiedDNSIP
from model.Practicalusing.UnifiedURL import UnifiedURL
from model.Practicalusing.URLtoDNS import URLtoDNS
from model.Practicalusing.counterlist import CounterList

#from model.advertising.tmpSolvePerson import TmpSolvePerson
from model.advertising.OperationHistory import OperationHistory
from model.advertising.Returnvaluedefine import ReturnValuedefine
from model.advertising.URL_advertisingarrival import AdvertisingArrival 
from model.advertising.result import ResultADUrl, ResultFastReg, ResultCounterStatus

def cmdbinit_model():
    ''' Call me before using any of the tables or classes in the model.'''

    try:
        cmetadata.create_all(cmengine)
        CMDBSession.commit()
    except:
        CMDBSession.rollback()
        raise
    finally:
        CMDBSession.commit()
        CMDBSession.close()
