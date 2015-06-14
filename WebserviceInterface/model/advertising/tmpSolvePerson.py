# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text, BIGINT
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['TmpSolvePerson']

class TmpSolvePerson(cmdeclarativeBase):
    __tablename__ = 'tmpsolveperson'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    Username = Column(String(200), nullable=False, default='0') 
    
    PhoneNum = Column(BIGINT, nullable=False, default=0)
    
    def __init__(self, Username, PhoneNum, id=0):
        self.id = id
        self.Username = Username
        self.PhoneNum = PhoneNum
        
    def __repr__(self):
        
        return '<TmpSolvePerson: id="%s", Username="%s", PhoneNum="%s">' % (self.id, self.Username, self.PhoneNum)
    
    