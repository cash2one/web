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

__all__ = ['EventCircuitRelation','EventCircultBasic','EventCircultStatus']

class EventCircuitRelation(declarativeBase):
    __tablename__ = 'eventcircuitrelation'
    
    # Columns
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Eid = Column(Integer, nullable=False, default=0)
    
    Cid = Column(Integer, nullable=False, default=0)
    
    def __init__(self, rid, Eid, Cid):
        self.rid = rid
        self.Eid = Eid
        self.Cid = Cid
        
    def __repr__(self):
        
        return '<EventCircuitRelation: rid="%s", Eid="%s", Cid="%s">' % (self.rid, self.Eid, self.Cid)
    
class EventCircultBasic(declarativeBase):
    __tablename__ = 'eventcircultbasic'
    
    # Columns
    Cid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    TakeoverPerson = Column(String(50), nullable=False, default=u'')
    
    Status = Column(Integer, nullable=False, default=0)
    
    SustainableTime = Column(Integer, nullable=False, default=24)
    
    CarePeopleCount = Column(Integer, nullable=False, default=0)
    
    def __init__(self, Cid, TakeoverPerson, Status, SustainableTime, CarePeopleCount):
        self.Cid = Cid
        self.TakeoverPerson = TakeoverPerson
        self.Status = Status
        self.SustainableTime = SustainableTime
        self.CarePeopleCount = CarePeopleCount
    
    def __repr__(self):
        
        return '<EventCircultBasic: Cid="%s", TakeoverPerson="%s", Status="%s", SustainableTime="%s", CarePeopleCount="%s">' % (self.Cid, self.TakeoverPerson, self.Status, self.SustainableTime, self.CarePeopleCount)
    
class EventCircultStatus(declarativeBase):
    __tablename__ = 'eventcircultstatus'
    
    # Columns
    StatusID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    StatusDesc = Column(String(20), unique=True, nullable=False, default=u'')
    
    def __init__(self, StatusID, StatusDesc):
        self.StatusID = StatusID
        self.StatusDesc = StatusDesc
        
    def __repr__(self):
        
        return '<EventCircultStatus: StatusID="%s", StatusDesc="%s">' % (self.StatusID, self.StatusDesc)
    
    