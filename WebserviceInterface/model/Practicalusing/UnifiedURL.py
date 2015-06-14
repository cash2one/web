# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.dialects.mssql import BIGINT, TINYINT
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['UnifiedURL']

class UnifiedURL(cmdeclarativeBase):
    __tablename__ = 'unifiedurl'
    __table_args__ = (UniqueConstraint('Url', 'Category', name='Url_Category_UK'), )
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    Url = Column(String(200), nullable=False, default=u'')
    
    Urlexplain = Column(String(200), nullable=False, default=u'')
    
    Category = Column(String(50), nullable=False, default=u'')
    
    Status = Column(TINYINT, nullable=False, default=0)
    
    def __init__(self, Url, Urlexplain, Category, Status, id=0):
        self.id = id
        self.Url = Url
        self.Urlexplain = Urlexplain
        self.Category = Category
        self.Status = Status
        
    def __repr__(self):
        
        return '<UnifiedURL: id="%s", Url="%s", Urlexplain="%s", Category="%s", Status="%s">' % (self.id, self.Url, self.Urlexplain, self.Category, self.Status)