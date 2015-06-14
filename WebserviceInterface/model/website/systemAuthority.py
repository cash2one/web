# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['SystemAuthority']

class SystemAuthority(declarativeBase):
    __tablename__ = 'websiteauthority'
    
    # Column
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True) 
    
    code = Column(String(50), nullable=False, default=u'')
    
    url_name = Column(String(50), nullable=False, default=u'')
    
    url = Column(String(255), nullable=False)
    
    def __init__(self, id, code, url_name, url):
        self.id = id
        self.code = code
        self.url_name = url_name
        self.url = url
        
    def __repr__(self):
        
        return '<SystemAuthority: id="%s", code="%s", url_name="%s", url="%s">' % (self.id, self.code, self.url_name, self.url)