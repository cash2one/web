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

__all__ = ['ZoneInform', 'ZonetoHost', 'ZoneInformByAMT']

class ZoneInform(declarativeBase):
    __tablename__ = 'zoneinform'
    __table_args__ = (UniqueConstraint('GameID', 'ZoneID', name='GameID_ZoneID_UK'), )
    
    # Column
    Rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)
    
    ZoneID = Column(Integer, nullable=False, default=0)
    
    ZoneName = Column(String(100), nullable=False, default=u'')
    
    ZoneDesc = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, Rid, GameID, ZoneID, ZoneName, ZoneDesc):
        self.Rid = Rid
        self.GameID = GameID
        self.ZoneID = ZoneID
        self.ZoneName = ZoneName
        self.ZoneDesc = ZoneDesc
        
    def __repr__(self):
        
        return '<ZoneInform: Rid="%s", GameID="%s", ZoneID="%s", ZoneName="%s", ZoneDesc="%s">' % (self.Rid, self.GameID, self.ZoneID, self.ZoneName, self.ZoneDesc)
    
class ZonetoHost(declarativeBase):
    __tablename__ = 'zonetohost'
    __table_args__ = (UniqueConstraint('zoneID', 'Hostname', name='zoneID_Hostname_UK'), )
    
    # Column
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    zoneID = Column(Integer, nullable=False, default=0)
    
    Hostname = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, rid, zoneID, Hostname):
        self.rid = rid
        self.zoneID = zoneID
        self.Hostname = Hostname
        
    def __repr__(self):
        
        return '<ZonetoHost: rid="%s", zoneID="%s", Hostname="%s">' % (self.rid, self.zoneID, self.Hostname)
    
class ZoneInformByAMT(declarativeBase):
    __tablename__ = 'zoneinformbyamt'
    __table_args__ = (UniqueConstraint('gamePYname', 'zonePYname', name='gamePYname_zonePYname_UK'), )
    
    # Column
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    gamename = Column(String(20), nullable=False, default='None')
    
    gamePYname = Column(String(50), nullable=False, default='None')
    
    zonename = Column(String(50), nullable=False, default='None')
    
    zonePYname = Column(String(50), nullable=False, default='None')
    
    Status = Column(Integer, nullable=False, default=0)
    
    def __init__(self, gamename, gamePYname, zonename, zonePYname, Status, id=0):
        self.id = id
        self.gamename = gamename
        self.gamePYname = gamePYname
        self.zonename = zonename
        self.zonePYname = zonePYname
        self.Status = Status
        
    def __repr__(self):
        
        return '<ZoneInformByAMT: id="%s", gamename="%s", gamePYname="%s", zonename="%s", zonePYname="%s", Status="%s">' % (self.id, self.gamename, self.gamePYname, self.zonename, self.zonePYname, self.Status)
    
    