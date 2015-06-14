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

__all__ = ['UnifiedDNSIP']

class UnifiedDNSIP(cmdeclarativeBase):
    __tablename__ = 'unifiednsip'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True) 
    
    Ipaddress = Column(String(64), nullable=False, default=u'')
    
    Status = Column(TINYINT, nullable=False, default=0)
    
    def __init__(self, Ipaddress, Status, id=0):
        self.id = id
        self.Ipaddress = Ipaddress
        self.Status = Status
        
    def __repr__(self):
        
        return '<UnifiedDNSIP: id="%s", Ipaddress="%s", Status="%s">' % (self.id, self.Ipaddress, self.Status)