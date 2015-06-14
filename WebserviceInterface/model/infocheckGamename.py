# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['InfoCheckGameName']

class InfoCheckGameName(declarativeBase):
    __tablename__ = 'infocheckgamename'
    
    # Columns
    
    infoName = Column(String(32), primary_key=True, nullable=False, default=u'')
    
    realName = Column(String(32), nullable=False, default=u'')
    
    def __init__(self, infoName, realName):
        self.infoName = infoName
        self.realName = realName
        
    def __repr__(self):
        
        return '<InfoCheckGameName: infoName="%s", realName="%s">' % (self.infoName, self.realName)
    