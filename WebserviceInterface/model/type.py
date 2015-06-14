# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

class TypeVarify(declarativeBase):
    __tablename__ = 'typevarify'
    
    # Column
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    name = Column(String(256), nullable=False, default=u'')
    
    srcUse = Column(Integer, nullable=False, default=0)
    
    dstUse = Column(Integer, nullable=False, default=0)
    
    desc = Column(String(256), nullable=False, default=u'')
    
    def __init__(self, id, name, srcUse, dstUse, desc):
        self.id = id
        self.name = name
        self.srcUse = srcUse
        self.dstUse = dstUse
        self.desc = desc
        
    def __repr__(self):
        
        return '<TypeVarify: id="%s", name="%s", srcUse="%s", dstUse="%s", desc="%s">' % (self.id, self.name, self.srcUse, self.dstUse, self.desc)