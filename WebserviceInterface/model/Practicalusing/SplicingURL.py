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

__all__ = ['SpliceURL']

class SpliceURL(cmdeclarativeBase):
    __tablename__ = 'spliceurl'
    
    # Column
    id = Column(Integer, primary_key=True, autoincrement=True) 
    
    Category = Column(String(50), nullable=False, default=u'')
    
    example = Column(Text, nullable=False)
    
    partipofurl = Column(TINYINT, nullable=False, default=0)
    
    def __init__(self, Category, example, partipofurl, id=0):
        self.id = id
        self.Category = Category
        self.example = example
        self.partipofurl = partipofurl
        
    def __repr__(self):
        
        return '<SpliceURL: id="%s", Category="%s", example="%s", partipofurl="%s">' % (self.id, self.Category, self.example, self.partipofurl)