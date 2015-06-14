# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['CarePeopleDetail']

class CarePeopleDetail(declarativeBase):
    __tablename__ = 'carepeopledetail'
    __table_args__ = (UniqueConstraint('Eid', 'Username', name='Eid_Username_UK'), )
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Eid = Column(Integer, nullable=False, default=0)
    
    Username = Column(String(100), nullable=False, default=u'')
    
    def __init__(self, id, Eid, Username):
        self.id = id
        self.Eid = Eid
        self.Username = Username
        
    def __repr__(self):
        
        return '<CarePeopleDetail: id="%s", Eid="%s", Username="%s">' % (self.id, self.Eid, self.Username)