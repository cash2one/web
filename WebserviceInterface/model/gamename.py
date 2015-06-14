# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

''' example : 'ZTQY': {'username': 'NDa1fxyv', 'password': 'iPQlacpVxeUr', 'ipaddress': '192.168.100.81', 'dbname': 'InfoServer_ZTQY', 'port': 3313} '''

__all__ = ['Gameinform']

class Gameinform(declarativeBase):
    __tablename__ = 'gamename'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    gameName = Column(String(20), nullable=False, unique=True, default=u'')
    
    host = Column(String(100), nullable=True)
    
    port = Column(Integer, nullable=True)
    
    dbName = Column(String(64), nullable=False, default=u'')
    
    def __init__(self, id, gameName, host, port, dbName):
        self.id = id
        self.gameName = gameName
        self.host = host
        self.port = port
        self.dbName = dbName
        
    def __repr__(self):
        
        return '<Gameinform: id="%s",  gameName="%s", host="%s", port="%s", dbName="%s">' % (self.id, self.gameName, self.host, self.port, self.dbName)