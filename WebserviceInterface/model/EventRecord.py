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

__all__ = ['EventRecord','EventRestoreResult','EventFinished']

class EventRecord(declarativeBase):
    __tablename__ = 'eventrecord'
    __table_args__ = (UniqueConstraint('EventID', 'opTimestamp', name='EventID_opTimestamp_UK'), )
    
    # Columns
    
    RecordID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    EventID = Column(Integer, nullable=False, default=0)
    
    nowStatus = Column(Integer, nullable=False, default=0)
    
    nextStatus = Column(Integer, nullable=False, default=0)
    
    opPeople = Column(String(32), nullable=False, default=u'')
    
    opTimestamp = Column(Integer, nullable=False, default=0)
    
    Remark = Column(Text, nullable=False)
    
    OccurTime = Column(Integer, nullable=False, default=0)
    
    deleteornot = Column(Integer, nullable=False, default=0)
    
    def __init__(self, RecordID, EventID, nowStatus, nextStatus, opPeople, opTimestamp, Remark, OccurTime, deleteornot):
        self.RecordID = RecordID
        self.EventID = EventID
        self.nowStatus = nowStatus
        self.nextStatus = nextStatus
        self.opPeople = opPeople
        self.opTimestamp = opTimestamp
        self.Remark = Remark
        self.OccurTime = OccurTime
        self.deleteornot = deleteornot
        
    def __repr__(self):
        
        return '<EventRecord: RecordID="%s", EventID="%s", nowStatus="%s", nextStatus="%s", opPeople="%s", opTimestamp="%s", Remark="%s", OccurTime="%s", deleteornot="%s">' % (self.RecordID, self.EventID, self.nowStatus, self.nextStatus, self.opPeople, self.opTimestamp, self.Remark, self.OccurTime, self.deleteornot)

class EventRestoreResult(declarativeBase):
    __tablename__ = 'eventrestoreresult'
    __table_args__ = (UniqueConstraint('EventID', 'OccurTime', name='EventID_OccurTime_UK'), )
    
    # Columns
    RestoreID = Column(Integer, primary_key=True, autoincrement=True)
    
    EventID = Column(Integer, nullable=False, default=0)
    
    WhoClose = Column(String(32), nullable=False, default=u'')
    
    OccurTime = Column(Integer, nullable=False, default=0)
    
    CloseTime = Column(Integer, nullable=False, default=0)
    
    DeleteorNot = Column(Integer, nullable=False, default=0)
    
    Detail = Column(Text, nullable=False)
    
    def __init__(self, EventID, WhoClose, OccurTime, CloseTime, DeleteorNot, Detail):
        self.EventID = EventID
        self.WhoClose = WhoClose
        self.OccurTime = OccurTime
        self.CloseTime = CloseTime
        self.DeleteorNot = DeleteorNot
        self.Detail = Detail
        
    def __repr__(self):
        
        return '<EventRestoreResult: RestoreID="%s", EventID="%s", WhoClose="%s", OccurTime="%s", CloseTime="%s", DeleteorNot="%s", Detail="%s">' % (RestoreID, self.EventID, self.WhoClose, self.OccurTime, self.CloseTime, self.DeleteorNot, self.Detail)

class EventFinished(declarativeBase):
    __tablename__ = 'eventfinished'
    __table_args__ = (UniqueConstraint('Eid', 'GameID', name='Eid_GameID_UK'), )
    
    # Columns 
    Rid = Column(Integer, primary_key=True, autoincrement=True)
    
    Eid = Column(Integer, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)
    
    Data = Column(Text, nullable=False)
    
    Oid = Column(String(50), nullable=False, default=u'0')
    
    OccurTime = Column(Integer, nullable=False, default=0)
    
    CloseTime = Column(Integer, nullable=False, default=0)
    
    DeleteorNot = Column(Integer, nullable=False, default=1)
    
    Detail = Column(Text, nullable=False)
    
    Username = Column(String(50), nullable=False, default='None')
    
    def __init__(self, Eid, GameID, Data, Oid, OccurTime, CloseTime, DeleteorNot, Detail, Username, Rid=0):
        self.Rid = Rid
        self.Eid = Eid
        self.GameID = GameID
        self.Data = Data
        self.Oid = Oid
        self.OccurTime = OccurTime
        self.CloseTime = CloseTime
        self.DeleteorNot = DeleteorNot
        self.Detail = Detail
        self.Username = Username
        
    def __repr__(self):
        
        return '<EventFinished: Rid="%s", Eid="%s", GameID="%s", Data="%s", Oid="%s", OccurTime="%s", CloseTime="%s", DeleteorNot="%s", Detail="%s", Username="%s">' % (self.Rid, self.Eid, self.GameID, self.Data, self.Oid, self.OccurTime, self.CloseTime, self.DeleteorNot, self.Detail, self.Username)