# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['EventOperation']

class EventOperation(declarativeBase):
    __tablename__ = 'eventoperation'
    
    # Columns
    Oid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    OName = Column(String(256), nullable=False, default=u'')
    
    OPYname = Column(String(256), nullable=False, default=u'')
    
    
    def __init__(self, Oid, OName, OPYname):
        self.Oid = Oid
        self.OName = OName
        self.OPYname = OPYname
        
    def __repr__(self):

        return '<EventOperation: Oid="%s", OName="%s", OPYname="%s">' % (self.Oid, self.OName, self.OPYname)