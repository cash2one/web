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

__all__ = ['ProcessInfo']

class ProcessInfo(declarativeBase):
    __tablename__ = 'processinfo'
    __table_args__ = (UniqueConstraint('ip', 'name', name='ip_name_UK'), )
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    ip = Column(String(16), nullable=False, default=u'')
    
    name = Column(String(255), nullable=False, default=u'')
    
    count = Column(Integer, nullable=False, default=u'')
    
    def __init__(self, id, ip, name, count):
        self.id = id
        self.ip = ip
        self.name = name
        self.count = count
        
    def __repr__(self):
        
        return '<ProcessInfo: id="%s", ip="%s", name="%s", count="%s">' % (self.id, self.ip, self.name, self.count)
    