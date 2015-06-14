# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['OidRequest', 'OIDVariable']

class OidRequest(declarativeBase):
    __tablename__ = 'oidRequest'
    
    # Column
    OID = Column(String(64), primary_key=True, nullable=False, default=u'1.0')
    
    VariablesRequest = Column(String(100), nullable=False, default=u'')
    
    VariablesOut = Column(String(100), nullable=False, default=u'')
    
    Nullable = Column(String(2), nullable=False, default=u'N')
    
    def __init__(self, OID, VariablesRequest, VariablesOut, Nullable):
        self.OID = OID
        self.VariablesRequest = VariablesRequest
        self.VariablesOut = VariablesOut
        self.Nullable = Nullable
        
    def __repr__(self):
        
        return '<OidRequest: OID="%s", VariablesRequest="%s", VariablesOut="%s", Nullable="%s">' % (self.OID, self.VariablesRequest, self.VariablesOut, self.Nullable)

class OIDVariable(declarativeBase):
    __tablename__ = 'oidVariable'
    
    # Column 
    variableName = Column(String(64), primary_key=True, nullable=False, default=u'') 
    
    struct = Column(String(20), nullable=False, default=u'')
    
    dataType = Column(String(20), nullable=False, default=u'')
    
    default = Column(String(20), nullable=False, default=u'')
    
    def __init__(self, variableName, struct, dataType, default):
        self.variableName = variableName
        self.struct = struct
        self.dataType = dataType
        self.default = default
        
    def __repr__(self):
        
        return '<OIDVariable: variableName="%s", struct="%s", dataType="%s", default="%s">'  % (self.variableName, self.struct, self.dataType, self.default)