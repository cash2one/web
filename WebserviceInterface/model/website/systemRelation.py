# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['SystemRelation']

class SystemRelation(declarativeBase):
    __tablename__ = 'websiteRoleAuthority'
    
    # Columns
    relationId = Column(Integer, primary_key=True, nullable=False, autoincrement=True) 
    
    roleId = Column(Integer, nullable=False, unique=True, default=0) 
    
    urlId = Column(Integer, nullable=False, unique=True, default=0)
    
    def __init__(self, relationId, roleId, urlId):
        self.relationId = relationId
        self.roleId = roleId
        self.urlId = urlId
        
    def __repr__(self):
        
        return '<SystemRelation: relationId="%s", roleId="%s", urlId="%s">' % (self.relationId, self.roleId, self.urlId)