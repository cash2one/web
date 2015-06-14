# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['AgenttoAssets','HosttoId','HardwareInfo','EthInfo']

class AgenttoAssets(declarativeBase):
    __tablename__ = 'agenttoassets'
    
    # Column
    Sid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Aid = Column(Integer, nullable=False, default=0)
    
    type = Column(String(100), nullable=False, default=u'')
    
    Hostname = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, Sid, Aid, type, Hostname):
        self.Sid = Sid
        self.Aid = Aid
        self.type = type
        self.Hostname = Hostname
        
    def __repr__(self):
        
        return '<AgenttoAssets: Sid="%s", Aid="%s", type="%s", Hostname="%s">' % (self.Sid, self.Aid, self.type, self.Hostname)
    
class HosttoId(declarativeBase):
    __tablename__ = 'hosttoid'
    
    #Column 
    Ownid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Hostname = Column(String(100), nullable=False, default=u'')
    
    Hid = Column(Integer, nullable=False, default=0)
    
    HStatus = Column(Integer, nullable=False, default=0)
    
    Eid = Column(Integer, nullable=False, default=0)
    
    EStatus = Column(Integer, nullable=False, default=1) 
    
    def __init__(self, Ownid, Hostname, Hid, HStatus, Eid, EStatus):
        self.Ownid = Ownid
        self.Hostname = Hostname
        self.Hid = Hid
        self.HStatus = HStatus
        self.Eid = Eid
        self.EStatus = EStatus
        
    def __repr__(self):
        
        return '<HosttoId: Ownid="%s", Hostname="%s", Hid="%s", HStatus="%s", Eid="%s", EStatus="%s">' % (self.Ownid, self.Hostname, self.Hid, self.HStatus, self.Eid, self.EStatus)
    

class HardwareInfo(declarativeBase):
    __tablename__ = 'hardwareinform'
    
    # Column
    Hid = Column(Integer, primary_key=True, nullable=False, default=0)
     
    Kernel = Column(String(100), nullable=False, default=u'')
    
    Model = Column(String(100), nullable=False, default=u'')
    
    CpuType = Column(String(100), nullable=False, default=u'')
    
    SN = Column(String(100), nullable=False, default=u'')
    
    ZCBM = Column(String(100), nullable=False, default=u'')
    
    CpuCoreNum = Column(String(100), nullable=False, default=u'')
    
    Memory = Column(String(100), nullable=False, default=u'')
    
    OS = Column(String(100), nullable=False, default=u'')
    
    Manufactuer = Column(String(100), nullable=False, default=u'')
    
    GameName = Column(String(20), nullable=False, default=u'')
    
    GameFunc = Column(String(20), nullable=False, default=u'')
    
    def __init__(self, Hid, Kernel, Model, CpuType, SN, ZCBM, CpuCoreNum, Memory, OS, Manufactuer, GameName, GameFunc):
        self.Hid = Hid
        self.Kernel = Kernel
        self.Model = Model
        self.CpuType = CpuType
        self.SN = SN
        self.ZCBM = ZCBM
        self.CpuCoreNum = CpuCoreNum
        self.Memory = Memory
        self.OS = OS
        self.Manufactuer = Manufactuer
        self.GameName = GameName
        self.GameFunc = GameFunc
    
    def __repr__(self):
        
        return '<HardwareInfo: Hid="%s", Kernel="%s", Model="%s", CpuType="%s", SN="%s", ZCBM="%s", CpuCoreNum="%s", Memory="%s", OS="%s", Manufactuer="%s", GameName="%s", GameFunc="%s">' % (self.Hid, self.Kernel, self.Model, self.CpuType, self.SN, self.ZCBM, self.CpuCoreNum, self.Memory, self.os, self.Manufactuer, self.GameName, self.GameFunc)
    
class EthInfo(declarativeBase):
    __tablename__ = 'ethinform'
    
    # Column
    eid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Eth0 = Column(String(100), nullable=False, default=u'')
    
    Eth1 = Column(String(100), nullable=False, default=u'')  
    
    Eth2 = Column(String(100), nullable=False, default=u'')
    
    Eth3 = Column(String(100), nullable=False, default=u'')   
    
    def __init__(self, eid, Eth0, Eth1, Eth2, Eth3):
        self.eid = eid
        self.Eth0 = Eth0
        self.Eth1 = Eth1
        self.Eth2 = Eth2
        self.Eth3 = Eth3
        
    def __repr__(self):
        
        return '<EthInfo: eid="%s", Eth0="%s", Eth1="%s", Eth2="%s", Eth3="%s">' % (self.eid, self.Eth0, self.Eth1, self.Eth2, self.Eth3)
    
class Ethdetail(declarativeBase):
    __tablename__ = 'ethdetail'
    __table_args__ = (UniqueConstraint('status', 'ip', name='status_ip_UK'), )
    
    # Column 
    eid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    status = Column(String(100), nullable=False, default=u'')
    
    ip = Column(String(100), nullable=False, default=u'')
    
    mask = Column(String(20), nullable=False, default=u'')    
    
    ethernet = Column(String(20), nullable=False, default=u'') 
    
    def __init__(self, eid, status, ip, mask, ethernet):
        self.eid = eid
        self.status = status
        self.ip = ip
        self.mask = mask
        self.ethernet = ethernet
        
    def __repr__(self):
        
        return '<Ethdetail: eid="%s", status="%s", ip="%s", mask="%s", ethernet="%s">' % (self.eid, self.status, self.ip, self.mask, self.ethernet)