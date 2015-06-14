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

__all__ = ['OidRepeat', 'OidControlTime']

class OidRepeat(declarativeBase):
    __tablename__ = 'oidrepeat'
    
    # Column 
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    content = Column(Text, nullable=False)
    
    oid = Column(String(20), nullable=False, default=u'')
    
    timestamp = Column(Integer, nullable=False, default=0)
    
    def __init__(self, content, oid, timestamp, id=0):
        self.id = id
        self.content = content
        self.oid = oid
        self.timestamp = timestamp
        
    def __repr__(self):
        
        return '<OidRepeat: id="%s", content="%s", oid="%s", timestamp="%s">' % (self.id, self.content, self.oid, self.timestamp)

class OidControlTime(declarativeBase):
    __tablename__ = 'oidcontroltime'
    
    # Column
    oid = Column(String(20), primary_key=True, nullable=False, default=0) 
    
    timeover = Column(Integer, nullable=False, default=0)
    
    Status = Column(Integer, nullable=False, default=0)
    
    def __init__(self, oid, timeover, Status):
        self.oid = oid
        self.timeover = timeover
        self.Status = Status
        
    def __repr__(self):
        
        return '<OidControlTime: oid="%s", timeover="%s", Status="%s">' % (self.oid, self.timeover, self.Status)    