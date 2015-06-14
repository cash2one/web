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

__all__ = ['EventLevel','EventAlarm']

class EventLevel(declarativeBase):
    __tablename__ = 'eventlevel'
    
    # Column
    eventLevelID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    levelExplain = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, eventLevelID, levelExplain):
        self.eventLevelID = eventLevelID
        self.levelExplain = levelExplain
        
    def __repr__(self):

        return '<EventLevel: eventLevelID="%s", levelExplain="%s">' % (self.eventLevelID, self.levelExplain)

class EventAlarm(declarativeBase):
    __tablename__ = 'eventalarm'
    __table_args__ = (UniqueConstraint('GameID', 'Timestamp', name='GameID_Timestamp_UK'), )
    
    # Column
    EiD = Column(Integer, primary_key=True, autoincrement=True)
    
    GameID = Column(Integer, nullable=False, default=0)
    
    eventGrade = Column(Integer, nullable=False, default=0)
    
    Data = Column(Text, nullable=False, default=u'')
    
    Timestamp = Column(Integer, nullable=False, default=0)
    
    Oid = Column(String(100), nullable=False, default=u'None')
    
    def __init__(self, GameID, eventGrade, Data, Timestamp, Oid, EiD=0):
        self.EiD = EiD
        self.GameID = GameID
        self.eventGrade = eventGrade
        self.Data = Data
        self.Timestamp = Timestamp
        self.Oid = Oid
    
    def __repr__(self):
        
        return '<EventAlarm: EiD="%s", GameID="%s", eventGrade="%s", Data="%s", Timestamp="%s", Oid="%s">' % (self.EiD, self.GameID, self.eventGrade, self.Data, self.Timestamp, self.Oid)
    
class EventAlarmDoing(declarativeBase):
    __tablename__ = 'eventalarmdoing'
    __table_args__ = (UniqueConstraint('Eid', 'NowStatus', name='Eid_NowStatus_UK'), )
    
    # Column
    Eid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)
    
    eventGrade = Column(Integer, nullable=False, default=0)
    
    Data = Column(Text, nullable=False, default=u'')
    
    Timestamp = Column(Integer, nullable=False, default=0)
    
    OccurTime = Column(Integer, nullable=False, default=0)
    
    Oid = Column(String(100), nullable=False, default=u'None')
    
    NowStatus = Column(Integer, nullable=False, default=1)
    
    EventName = Column(String(200), nullable=False, default=u'None')
    
    def __init__(self, Eid, GameID, eventGrade, Data, Timestamp, OccurTime, Oid, NowStatus, EventName):
        self.Eid = Eid
        self.GameID = GameID
        self.eventGrade = eventGrade
        self.Data = Data
        self.Timestamp = Timestamp
        self.OccurTime = OccurTime
        self.Oid = Oid
        self.NowStatus = NowStatus
        self.EventName = EventName
    
    def __repr__(self):
        
        return '<EventAlarm: Eid="%s", GameID="%s", eventGrade="%s", Data="%s", Timestamp="%s", OccurTime="%s", Oid="%s", NowStatus="%s", EventName="%s">' % (self.Eid, self.GameID, self.eventGrade, self.Data, self.Timestamp, self.OccurTime, self.Oid, self.NowStatus, self.EventName)