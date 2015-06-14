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

__all__ = ['URLtoDNS']

class URLtoDNS(cmdeclarativeBase):
    __tablename__ = 'URL_Dns'
    __table_args__ = (UniqueConstraint('urlid', 'dnsid', name='urlid_dnsid_UK'), )
    
    # Columns
    rid = Column(Integer, primary_key=True, autoincrement=True) 
    
    urlid = Column(TINYINT, nullable=False, default=0)
    
    dnsid = Column(TINYINT, nullable=False, default=0)
    
    def __init__(self, urlid, dnsid, rid=0):
        self.rid = rid
        self.urlid = urlid
        self.dnsid = dnsid
        
    def __repr__(self):
        
        return '<URLtoDNS: rid="%s", urlid="%s", dnsid="%s">' % (self.rid, self.urlid, self.dnsid)
    
    
        
        