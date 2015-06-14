# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['EventRelation', 'EventInterrlated']

class EventRelation(declarativeBase):
    __tablename__ = 'eventrelation'
    
    #Column 
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    OID = Column(String(100), unique=True, nullable=False, default=u'')
    
    eventType = Column(Integer, nullable=False, default=0)
    
    eventVar = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, id, OID, eventType, eventVar):
        self.id = id
        self.OID = OID
        self.eventType = eventType
        self.eventVar = eventVar
    
    def __repr__(self):
        
        return '<EventRelation: id="%s", OID="%s", eventType="%s", eventVar="%s">' % (self.id, self.OID, self.eventType, self.eventVar)

class EventInterrlated(declarativeBase):
    __tablename__ = 'eventinterrlated'
    
    # Column 
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    sourceOID = Column(String(100), nullable=False, default=u'')
    
    destOID = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, id, sourceOID, destOID):
        self.id = id
        self.sourceOID = sourceOID
        self.destOID = destOID
    
    def __repr__(self):
        
        return '<EventInterrlated: id="%s", sourceOID="%s", destOID="%s">' % (self.id, self.sourceOID, self.destOID)