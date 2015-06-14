# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['CounterList']

class CounterList(cmdeclarativeBase):
    __tablename__ = 'counterlist'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    ipaddress = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, ipaddress, id=0):
        self.id = id
        self.ipaddress = ipaddress
        
    def __repr__(self):
        
        return '<CounterList: id="%s", ipaddress="%s">' % (self.id, self.ipaddress)
    