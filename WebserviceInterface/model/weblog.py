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

__all__ = ['WebLog']

class WebLog(declarativeBase):
    __tablename__ = 'weblog'
    __table_args__ = (UniqueConstraint('Username', 'Timestamp', name='Username_Timestamp_UK'), )
    
    # Columns
    Nid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Username = Column(String(50), nullable=False, default=u'')
    
    Timestamp = Column(Integer, nullable=False, default=0)
    
    TableName = Column(String(50), nullable=False, default=u'')
    
    Data = Column(Text, nullable=False)
    
    Status = Column(String(20), nullable=False, default=0)
    
    def __init__(self, Nid, Username, Timestamp, TableName, Data, Status):
        self.Nid = Nid
        self.Username = Username
        self.Timestamp = Timestamp
        self.TableName = TableName
        self.Data = Data
        self.Status = Status
        
    def __repr__(self):
        
        return '<WebLog: Nid="%s", Username="%s", Timestamp="%s", TableName="%s", Data="%s", Status="%s">' % (self.Nid, self.Username, self.Timestamp, self.TableName, self.Data, self.Status)