# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['Template']

class Template(declarativeBase):
    __tablename__ = 'template'
    
    # Column
    TemplateID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    TemplateName = Column(String(64), nullable=False, unique=True, default=u'')
    
    TemplateType = Column(String(64), nullable=False, default=u'Agent')
    
    OIDType = Column(String(64), nullable=False, default=u'snmpget')
    
    OID = Column(String(100), nullable=False, default=u'')
    
    Timeout = Column(Integer, nullable=False, default=0)
    
    Cron = Column(Integer, nullable=False, default=60)
    
    Do = Column(String(64), nullable=False, default=u'Agent')
    
    Forward = Column(Integer, nullable=False, default=1)
    
    def __init__(self, TemplateID, TemplateName, TemplateType, OIDType, OID, Timeout, Cron, Do, Forward):
        self.TemplateID = TemplateID
        self.TemplateName = TemplateName
        self.TemplateType = TemplateType
        self.OIDType = OIDType
        self.OID = OID
        self.Timeout = Timeout
        self.Cron = Cron
        self.Do = Do
        self.Forward = Forward
        
    def __repr__(self):
        
        return '<Template: TemplateID="%s", TemplateName="%s", TemplateType="%s", OIDType="%s", OID="%s", Timeout="%s", Cron="%s", Do="%s", Forward="%s">' % (self.TemplateID, self.TemplateName, self.TemplateType, self.OIDType, self.OID, self.Timeout, self.Cron, self.Do, self.Forward)
    
