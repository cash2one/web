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

__all__ = ['ReturnValuedefine']

class ReturnValuedefine(cmdeclarativeBase):
    __tablename__ = 'returnvaluedefine'
    __table_args__ = (UniqueConstraint('value', 'Type', name='value_Type_UK'), )
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    value = Column(Integer, nullable=False, default=0)
    
    ZHdefine = Column(Text, nullable=False, default='')
    
    Type = Column(String(100), nullable=False, default=u'None')
    
    Status = Column(Integer, nullable=False, default=0)
    
    def __init__(self, value, ZHdefine, Type, Status, id=0):
        self.id = id
        self.value = value
        self.ZHdefine = ZHdefine
        self.Type = Type
        self.Status = Status
    
    def __repr__(self):
        
        return '<ReturnValuedefine: id="%s", value="%s", ZHdefine="%s", Type="%s", Status="%s">' % (self.id, self.value, self.ZHdefine, self.Type, self.Status)
    
    