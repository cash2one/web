# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['EventTransportDefine']

class EventTransportDefine(declarativeBase):
    __tablename__ = 'eventtransportdefine'
    
    # Columns
    # 序列ID
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    # 流程ID
    Tid = Column(Integer, nullable=False, default=0)
    
    # 流程equal
    Tequal = Column(Integer, nullable=False, default=-1)
    
    # 流程before
    Tbefore = Column(Integer, nullable=False, default=-1)
    
    # 流程next
    Tnext = Column(Integer, nullable=False, default=-1)
    
    # 流程回滚
    Trollback = Column(Integer, nullable=False, default=-1)

    def __init__(self, id, Tid, Tequal, Tbefore, Tnext, Trollback):
        self.id = id
        self.Tid = Tid
        self.Tequal = Tequal
        self.Tbefore = Tbefore
        self.Tnext = Tnext
        self.Trollback = Trollback
        
    def __repr__(self):
        
        return '<EventTransportDefine: id="%s", Tid="%s", Tequal="%s", Tbefore="%s", Tnext="%s", Trollback="%s">' % (self.id, self.Tid, self.Tequal, self.Tbefore, self.Tnext, self.Trollback)