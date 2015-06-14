# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['Translate']

class Translate(declarativeBase):
    __tablename__ = 'translate'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, default=0)
    
    simple = Column(String(255), nullable=False, unique=True, default=u'None')
    
    detail = Column(String(255), nullable=False, default=u'None')
    
    def __init__(self, id, simple, detail):
        
        self.id = id
        self.simple = simple
        self.detail = detail
        
    def __repr__(self):
        
        return '<Translate: id="%s", simple="%s", detail="%s">' % (self.id, self.simple, self.detail)
    
    