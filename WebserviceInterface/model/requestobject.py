# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['AgentList','SwitchList','NodeList']

class AgentList(declarativeBase):
    __tablename__ = 'AgentList'
    
    # Columns
    AgentID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    AgentZone = Column(Integer, nullable=False, default=u'NULL')
    
    AgentName = Column(String(64), nullable=False, default=u'')
    
    IP = Column(String(64), nullable=False, default=u'')
    
    Port = Column(String(64), nullable=False, default=u'')
    
    IsUse = Column(Integer, nullable=False, default=1)
    
    def __init__(self, AgentID, AgentZone, AgentName, IP, Port, IsUse):

        self.AgentID = AgentID
        self.AgentZone = AgentZone
        self.AgentName = AgentName
        self.IP = IP
        self.Port = Port
        self.IsUse = IsUse
        
    def __repr__(self):
        
        return '<AgentList: AgentID="%s", AgentZone="%s", AgentName="%s", IP="%s", Port="%s", IsUse="%">' % (self.AgentID, self.AgentZone, self.AgentName, self.IP, self.Port, self.IsUse)

class SwitchList(declarativeBase):
    __tablename__ = 'SwitchList'
    
    # Columns
    SwitchID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    SwitchZone = Column(Integer, nullable=False, default=u'NULL')
    
    SwitchName = Column(Integer, nullable=False, default=u'')
    
    IP = Column(String(64), nullable=False, default=u'')
    
    SnmpUser = Column(Integer, nullable=False, default=u'')
    
    SnmpPass = Column(Integer, nullable=False, default=u'')
    
    IsUse = Column(Integer, nullable=False, default=1)
    
    def __init__(self, SwitchID, SwitchZone, SwitchName, IP, SnmpUser, SnmpPass, IsUse):
        
        self.SwitchID = SwitchID
        self.SwitchZone = SwitchZone
        self.SwitchName = SwitchName
        self.IP = IP
        self.SnmpUser = SnmpUser
        self.SnmpPass = SnmpPass
        self.IsUse = IsUse
        
    def __repr__(self):
        
        return '<SwitchList: SwitchID="%s", SwitchZone="%s", SwitchName="%s", IP="%s", SnmpUser="%s", SnmpPass="%s", IsUse="%s">' % (self.SwitchID, self.SwitchZone, self.SwitchName, self.IP, self.SnmpUser, self.SnmpPass, self.IsUse)
    
class NodeList(declarativeBase):
    __tablename__ = 'NodeList'
    
    # Columns
    NodeID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    NodeType = Column(Integer, nullable=False, default=0)
    
    NodeZone = Column(String(64), nullable=False, default=u'NULL')
    
    NodeName = Column(String(64), nullable=False, default=u'')
    
    IP = Column(String(64), nullable=False, default=u'')
    
    Port = Column(String(64), nullable=False, default=u'')
    
    Info = Column(String(64), nullable=True, default=u'')
    
    IsUse = Column(Integer, nullable=False, default=1)
    
    def __init__(self, NodeID, NodeType, NodeZone, NodeName, IP, Port, Info, IsUse):
        
        self.NodeID = NodeID
        self.NodeType = NodeType
        self.NodeZone = NodeZone
        self.NodeName = NodeName
        self.IP = IP
        self.Port = Port
        self.Info = Info
        self.IsUse = IsUse
        
    def __repr__(self):
        
        return '<NodeList: NodeID="%s", NodeType="%s", NodeZone="%s", NodeName="%s", IP="%s", Port="%s", Info="%s", IsUse="%s">' % (self.NodeID, self.NodeType, self.NodeZone, self.NodeName, self.IP, self.Port, self.Info, self.IsUse)
    
        