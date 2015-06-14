# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['ADuser']

class ADuser(declarativeBase):
    __tablename__ = 'aduser'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    username = Column(String(256), nullable=False, default=u'')
    
    password = Column(String(256), nullable=False, default=u'')
    
    validateTime = Column(Integer, nullable=False, default=0)
    
    def __init__(self, id, username, password, validateTime):
        
        self.id = id
        self.username = username
        self.password = password
        self.validateTime = validateTime
        
    def __repr__(self):
        
        return '<ADuser: id="%s", username="%s", password="%s", validateTime="%s">' % (self.id, self.username, self.password, self.validateTime)
