# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['CommandType','CommandTypeRelation']

class CommandType(declarativeBase):
    __tablename__ = 'command_type'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    command = Column(String(5), nullable=False, default=u'')
    
    command_type = Column(String(32), nullable=False, default=u'')
    
    def __init__(self, id, command, command_type):
        
        self.id = id
        self.command = command
        self.command_type = command_type
        
    def __repr__(self):
        
        return '<CommandType: id="%s", command="%s", command_type="%s">' % (self.id, self.command, self.command_type)

class CommandTypeRelation(declarativeBase):
    __tablename__ = 'command_type_relation'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    serverID = Column(Integer, nullable=False, default=0)
    
    clientID = Column(Integer, nullable=False, default=0)
    
    def __init__(self, id, serverID, clientID):
        
        self.id = id
        self.serverID = serverID
        self.clientID = clientID
    
    def __repr__(self):
        
        return '<CommandTypeRelation: id="%s", serverID="%s", clientID="%s">' % (self.id, self.serverID, self.clientID)