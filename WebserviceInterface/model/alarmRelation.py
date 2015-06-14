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

__all__ = ['AlarmRelation','ProjecttoGroup']

class AlarmRelation(declarativeBase):
    __tablename__ = 'AlarmRelation'
    
    # Column
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    uid = Column(Integer, nullable=False, default=0)

    ulevel = Column(Integer, nullable=False, default=0)
    
    gid = Column(Integer, nullable=False, default=0)
    
    def __init__(self, rid, uid, ulevel, gid):
        self.rid = rid
        self.uid = uid
        self.ulevel = ulevel
        self.gid = gid
        
    def __repr__(self):
        
        return '<AlarmRelation: rid="%s", uid="%s", ulevel="%s", gid="%s">' % (self.rid, self.uid, self.ulevel, self.gid)
    
class ProjecttoGroup(declarativeBase):
    __tablename__ = 'projecttogroup'
    
    # Column
    rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    gameID = Column(Integer, nullable=False, default=0)
    
    groupID = Column(Integer, nullable=False, default=0)
    
    ''' UniqueConstraint Usage '''
    __table_args__ = (UniqueConstraint('gameID', 'groupID', name='gameID_groupID_UK'), )
    
    def __init__(self, rid, gameID, groupID):
        self.rid = rid
        self.gameID = gameID
        self.groupID = groupID
        
    def __repr__(self):
        
        return '<ProjecttoGroup: rid="%s", gameID="%s", groupID="%s">' % (self.rid, self.gameID, self.groupID)