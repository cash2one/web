# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['DesigntoOther']

class DesigntoOther(declarativeBase):
    __tablename__ = 'designtoother'
    __table_args__ = (UniqueConstraint('EventID', 'opTimestamp', name='EventID_opTimestamp_UK'), )
    
    # Columns
    RID = Column(Integer, primary_key=True, autoincrement=True)
    
    EventID = Column(Integer, nullable=False, default=0) 
    
    FromUser = Column(String(64), nullable=False, default=u'')
    
    ToUser = Column(String(64), nullable=False, default=u'')
    
    opTimestamp = Column(Integer, nullable=False, default=0)
    
    NowStatus = Column(Integer, nullable=False, default=0)
    
    Remark = Column(Text, nullable=False)
    
    def __init__(self, EventID, FromUser, ToUser, opTimestamp, NowStatus, Remark, RID=0):
        self.RID = RID
        self.EventID = EventID
        self.FromUser = FromUser
        self.ToUser = ToUser
        self.opTimestamp = opTimestamp
        self.NowStatus = NowStatus
        self.Remark = Remark
        
    def __repr__(self):
        
        return '<DesigntoOther: RID="%s", EventID="%s", FromUser="%s", ToUser="%s", opTimestamp="%s", NowStatus="%s", Remark="%s">' % (self.RID, self.EventID, self.FromUser, self.ToUser, self.opTimestamp, self.NowStatus, self.Remark)   