# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['AdvertisingArrival']

class AdvertisingArrival(cmdeclarativeBase):
    __tablename__ = 'advertisingarrival'
    __table_args__ = (UniqueConstraint('url', 'Project', name='url_Project_UK'), )
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    url = Column(String(200), nullable=False, default=u'None')
    
    StartTimestamp = Column(Integer, nullable=False, default=0)
    
    OverTimestamp = Column(Integer, nullable=False, default=0)

    Status = Column(Integer, nullable=False, default=0)
    
    Project = Column(String(20), nullable=False, default=u'0')
    
    pagealias = Column(String(100), nullable=False, default=u'None')
    
    def __init__(self, url, StartTimestamp, OverTimestamp, Status, Project, pagealias, id=0):
        self.id = id
        self.url = url
        self.StartTimestamp = StartTimestamp
        self.OverTimestamp = OverTimestamp
        self.Status = Status
        self.Project = Project
        self.pagealias = pagealias
        
    def __repr__(self):
        
        return '<AdvertisingArrival: id="%s", url="%s", StartTimestamp="%s", OverTimestamp="%s", Status="%s", Project="%s"， pagealias="%s">' % (self.id, self.url, self.StartTimestamp, self.OverTimestamp, self.Status, self.Project, self.pagealias)