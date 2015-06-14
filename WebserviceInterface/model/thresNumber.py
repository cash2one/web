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

__all__ = ['ThresNumber','ThresRelation']

class ThresNumber(declarativeBase):
    __tablename__ = 'thresnumber'
    
    # Column
    thresID = Column(Integer, primary_key=True, nullable=False, default=0)

    thresLevel = Column(Integer, nullable=False, default=0)
    
    thresValueOne = Column(String(100), nullable=True, default=u'')
    
    thresValueTwo = Column(String(100), nullable=True, default=u'')

    def __init__(self, thresID, thresLevel, thresValueOne, thresValueTwo):
        self.thresID = thresID
        self.thresLevel = thresLevel
        self.thresValueOne = thresValueOne
        self.thresValueTwo = thresValueTwo
        
    def __repr__(self):
        
        return '<ThresNumber: thresID="%s", thresLevel="%s", thresValueOne="%s", thresValueTwo="%s">' % (self.thresID, self.thresLevel, self.thresValueOne, self.thresValueTwo)
    
class ThresRelation(declarativeBase):
    __tablename__ = 'thresrelation'
    
    # Column
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    gameid = Column(Integer, nullable=False, default=0)
    
    thresType = Column(String(100), nullable=False, default=u'')
    
    ThresNumberID = Column(Integer, nullable=False, default=0)
    
    ''' UniqueConstraint Usage '''
    __table_args__ = (UniqueConstraint('gameid', 'thresType', name='gameid_thresType_UK'), )
    
    def __init__(self, rid, gameid, thresType, ThresNumberID):
        self.rid = rid
        self.gameid = gameid
        self.thresType = thresType
        self.ThresNumberID = ThresNumberID
        
    def __repr__(self):
        
        return '<ThresRelation: rid="%s", gameid="%s", thresType="%s", ThresNumberID="%s">' % (self.rid, self.gameid, self.thresType, self.ThresNumberID)
 