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

__all__ = ['AssetForAgent','AssetidtoEid']

class AssetForAgent(declarativeBase):
    __tablename__ = 'assetforagent'
    __table_args__ = (UniqueConstraint('ZCBM', 'Timestamp', name='ZCBM_Timestamp_UK'), )
    
    # Columns
    Hid = Column(Integer, primary_key=True, autoincrement=True)
    
    ProjectName = Column(String(100), nullable=False, default=u'')
    
    ProjectFunc = Column(String(100), nullable=False, default=u'')
    
    Kernel = Column(String(100), nullable=False, default=u'0')
    
    CpuCoreNum = Column(String(5), nullable=False, default=u'')
    
    SerialNum = Column(String(20), nullable=False, default=u'')
    
    ZCBM = Column(String(10), nullable=False, default=u'0')
    
    Memory = Column(String(200), nullable=False, default=u'')
    
    CpuType = Column(String(100), nullable=False, default=u'')
    
    Model = Column(String(100), nullable=False, default=u'')
    
    HostName = Column(String(50), nullable=False, default=u'')
    
    OS = Column(String(200), nullable=False, default=u'')
    
    Manufacturer = Column(String(100), nullable=False, default=u'')
    
    Timestamp = Column(Integer, nullable=False, default=0)
    
    def __init__(self, ProjectName, ProjectFunc, Kernel, CpuCoreNum, SerialNum, ZCBM, Memory, CpuType, Model, HostName, OS, Manufacturer, Timestamp, Hid=0):
        self.Hid = Hid
        self.ProjectName = ProjectName
        self.ProjectFunc = ProjectFunc
        self.Kernel = Kernel
        self.CpuCoreNum = CpuCoreNum
        self.SerialNum = SerialNum
        self.ZCBM = ZCBM
        self.Memory = Memory
        self.CpuType = CpuType
        self.Model = Model
        self.HostName = HostName
        self.OS = OS
        self.Manufacturer = Manufacturer
        self.Timestamp = Timestamp
        
    def __repr__(self):
        
        return '<AssetForAgent: Hid="%s", ProjectName="%s", ProjectFunc="%s", Kernel="%s", CpuCoreNum="%s", SerialNum="%s", ZCBM="%s", Memory="%s", CpuType="%s", Model="%s", HostName="%s", OS="%s", Manufacturer="%s", Timestamp="%s">' % (self.Hid, self.ProjectName, self.ProjectFunc, self.Kernel, self.CpuCoreNum, self.SerialNum, self.ZCBM, self.Memory, self.CpuType, self.Model, self.HostName, self.OS, self.Manufacturer, self.Timestamp)
    
class AssetidtoEid(declarativeBase):
    __tablename__ = 'assetidtoeid'
    __table_args__ = (UniqueConstraint('assetid', 'eid', name='assetid_eid_UK'), )
    
    # Columns
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    assetid = Column(Integer, nullable=False, default=0)
    
    eid = Column(Integer, nullable=False, default=0)
    
    def __init__(self, rid, assetid, eid):
        self.rid = rid
        self.assetid = assetid
        self.eid = eid
        
    def __repr__(self):
        
        return '<AssetidtoEid: rid="%s", assetid="%s", eid="%s">' % (self.rid, self.assetid, self.eid)