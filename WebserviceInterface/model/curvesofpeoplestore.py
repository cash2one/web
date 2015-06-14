# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['CurvesOfpeopleStore']

class CurvesOfpeopleStore(declarativeBase):
    __tablename__ = 'curvesofpeoplestore'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True) 
    
    message = Column(Text, nullable=False)
    
    timestamp = Column(Integer, nullable=False, default=0)
    
    def __init__(self, message, timestamp, id=0):
        self.id = id
        self.message = message
        self.timestamp = timestamp
        
    def __repr__(self):
        
        return '<CurvesOfpeopleStore: id="%s", message="%s", timestamp="%s">' % (self.id, self.message, self.timestamp)
    
    
