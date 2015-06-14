# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['HostnameToProcess', 'ProcessStandard', 'TempProcess']

class HostnameToProcess(declarativeBase):
    __tablename__ = 'hostnametoprocess'
    __table_args__ = (UniqueConstraint('Hostname', 'Process', name='Hostname_Process_UK'), )
    
    # Columns
    Hid = Column(Integer, primary_key=True, autoincrement=True)
    
    Hostname = Column(String(50), nullable=False, default=u'')
    
    Process = Column(String(100), nullable=False)
    
    def __init__(self, Hid, Hostname, Process):
        self.Hid = Hid
        self.Hostname = Hostname
        self.Process = Process
        
    def __repr__(self):
        
        return '<HostnameToProcess: Hid="%s", Hostname="%s", Process="%s">' % (self.Hid, self.Hostname, self.Process)
    
class ProcessStandard(declarativeBase):
    __tablename__ = 'processstandard'
    
    # Column
    pid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)
    
    pIndex = Column(Text, nullable=False)
    
    pIgnore = Column(Text, nullable=False)
    
    def __init__(self, pid, GameID, pIndex, pIgnore):
        self.pid = pid
        self.GameID = GameID
        self.pIndex = pIndex
        self.pIgnore = pIgnore
        
    def __repr__(self):
        
        return '<ProcessStandard: pid="%s", GameID="%s", pIndex="%s", pIngore="%s">' % (self.pid, self.GameID, self.pIndex, self.pIgnore)   
    
class TempProcess(declarativeBase):
    __tablename__ = 'tempprocess'
    
    # Columns
    tempID = Column(Integer, primary_key=True, autoincrement=True)
    
    Ipaddress = Column(String(60), nullable=False, default=u'')
    
    Process = Column(Text, nullable=False)
    
    TimeStamp = Column(Integer, nullable=False, default=0)
    
    def __init__(self, Ipaddress, Process, TimeStamp, tempID=0):
        self.tempID = tempID
        self.Ipaddress = Ipaddress
        self.Process = Process
        self.TimeStamp = TimeStamp
        
    def __repr__(self):
        
        return '<TempProcess: tempID="%s", Ipaddress="%s", Process="%s", TimeStamp="%s">' % (self.tempID, self.Ipaddress, self.Process, self.TimeStamp)