# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['CURVES','CurvesIgnore']

class CURVES(declarativeBase):
    __tablename__ = 'curves'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    name = Column(String(32), nullable=False, default=u'')
    
    host = Column(String(256), nullable=False, default=u'')
    
    port = Column(Integer, nullable=False, default=0)
    
    database = Column(String(256), nullable=False, default=u'')
    
    def __init__(self, id, name, host, port, database):
        
        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.database = database
        
    def __repr__(self):
        
        return '<CURVES: id="%s", name="%s", host="%s", port="%s", database="%s">' % (self.id, self.name, self.host, self.port, self.database)
    
class CurvesIgnore(declarativeBase):
    __tablename__ = 'curvesignore'
    
    # Columns
    IgnoreID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Category = Column(String(256), nullable=False, default=u'')
    
    gameID = Column(Integer, nullable=False, default=0)
    
    def __init__(self, IgnoreID, Category, gameID):
        self.IgnoreID = IgnoreID
        self.Category = Category
        self.gameID = gameID
    
    def __repr__(self):
        
        return '<CurvesIgnore: IgnoreID="%s", Category="%s", gameID="%s">' % (self.IgnoreID, self.Category, self.gameID)