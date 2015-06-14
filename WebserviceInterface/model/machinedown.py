# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['MachineDown']

class MachineDown(declarativeBase):
    __tablename__ = 'machinedowntime'
    
    # Column
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    ZCBM = Column(String(10), nullable=False, default=u'0')
    
    HostName = Column(String(50), nullable=False, default=u'')
    
    Project = Column(String(100), nullable=False, default=u'')
    
    Timestamp = Column(Integer, nullable=False, default=0)
    
    def __init__(self, ZCBM, HostName, Project, Timestamp, id=0):
        self.id = id
        self.ZCBM = ZCBM
        self.HostName = HostName
        self.Project = Project
        self.Timestamp = Timestamp
        
    def __repr__(self):
        
        return '<MachineDown: id="%s", ZCBM="%s", HostName="%s", Project="%s", Timestamp="%s">' % (self.id, self.ZCBM, self.HostName, self.Project, self.Timestamp)
    