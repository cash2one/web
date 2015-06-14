# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['SystemRole']

class SystemRole(declarativeBase):
    __tablename__ = 'websiterole'

    # Columns
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False) 
    
    group_name = Column(String(25), nullable=False)
    
    def __init__(self, id, group_name):
        self.id = id
        self.group_name = group_name
        
    def __repr__(self):
        
        return '<SystemRole: id="%s", group_name="%s">' % (self.id, self.group_name)