# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['ResultCounterStatus','ResultFastReg','ResultADUrl']

class ResultCounterStatus(cmdeclarativeBase):
    __tablename__ = 'resultcounterstatus'
    
    # Columns
    Status = Column(String(20), primary_key=True, nullable=False, default='False') 
    
    Char = Column(String(200), nullable=False, default='None')
    
    SolvePerson = Column(String(100), nullable=False, default='None') 
    
    def __init__(self, Status, Char, SolvePerson):
        self.Status = Status
        self.Char = Char
        self.SolvePerson = SolvePerson
        
    def __repr__(self):
        
        return '<ResultCounterStatus: Status="%s", Char="%s", SolvePerson="%s">' % (self.Status, self.Char, self.SolvePerson)
    
class ResultFastReg(cmdeclarativeBase):
    __tablename__ = 'resultfastreg'
    
    # Columns
    Status = Column(String(20), primary_key=True, nullable=False, default='False') 
    
    Char = Column(Text, nullable=False)
    
    SolvePerson = Column(String(100), nullable=False, default='None') 
    
    def __init__(self, Status, Char, SolvePerson):
        self.Status = Status
        self.Char = Char
        self.SolvePerson = SolvePerson
        
    def __repr__(self):
        
        return '<ResultFastReg: Status="%s", Char="%s", SolvePerson="%s">' % (self.Status, self.Char, self.SolvePerson)
    
class ResultADUrl(cmdeclarativeBase):
    __tablename__ = 'resultadurl'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    project = Column(String(20), nullable=False, default='None')
    
    overtime = Column(String(50), nullable=False, default='0') 
    
    starttime = Column(String(50), nullable=False, default='0')
    
    url = Column(Text, nullable=False)
    
    pagealias = Column(Text, nullable=False)
    
    Status = Column(String(50), nullable=False, default='False')
    
    def __init__(self, project, overtime, starttime, url, pagealias, Status, id=0):
        self.id = id
        self.project = project
        self.overtime = overtime
        self.starttime = starttime
        self.url = url
        self.pagealias = pagealias
        self.Status = Status
        
    def __repr__(self):
        
        return '<ResultADUrl: id="%s", project="%s", overtime="%s", starttime="%s", url="%s", pagealias="%s", Status="%s">' % (self.id, self.project, self.overtime, self.starttime, self.url, self.pagealias, self.Status)