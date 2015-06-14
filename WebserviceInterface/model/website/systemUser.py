# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, BigInteger
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy.dialects.mssql import BIGINT, TINYINT

__all__ = ['SystemUser']

class SystemUser(declarativeBase):
    __tablename__ = 'websiteusers'
    
    # Columns
    id =  Column(Integer, primary_key=True, nullable=False, autoincrement=False) 
    
    name = Column(String(25), nullable=False)
    
    passwd = Column(String(25), nullable=False)
    
    is_active =  Column(TINYINT, nullable=False)
    
    role_id = Column(BIGINT, nullable=False)
    
    def __init__(self, id, name, passwd, is_active, role_id):
        self.id = id
        self.name = name
        self.passwd = passwd
        self.is_active = is_active
        self.role_id = role_id
        
    def __repr__(self):
        
        return '<SystemUser: id="%s", name="%s", passwd="%s", is_active="%s", role_id="%s">' % (self.id, self.name, self.passwd, self.is_active, self.role_id)