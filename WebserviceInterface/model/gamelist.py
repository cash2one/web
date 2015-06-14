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

__all__ = ['GameList','GameListtoArea','GameGroupRelation']

class GameList(declarativeBase):
    __tablename__ = 'GameList'
    
    # Column 
    GameID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Name = Column(String(64), nullable=False, default=u'')
    
    FullName = Column(String(100), nullable=False, default=u'')
    
    IsUse = Column(Integer, nullable=False, default=1)
    
    def __init__(self, GameID, Name, FullName, IsUse):
        self.GameID = GameID
        self.Name = Name
        self.FullName = FullName
        self.IsUse = IsUse
        
    def __repr__(self):
        
        return '<GameList: GameID="%s", Name="%s", FullName="%s", IsUse="%s">' % (self.GameID, self.Name, self.FullName, self.IsUse)
    
class GameListtoArea(declarativeBase):
    __tablename__ = 'gamelisttoarea'
    
    # Columns
    Rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)  
    
    ZoneID = Column(Integer, nullable=False, default=0)
    
    ''' UniqueConstraint Usage '''
    __table_args__ = (UniqueConstraint('GameID', 'ZoneID', name='GameID_ZoneID_UK'), )
    
    def __init__(self, Rid, GameID, ZoneID):
        self.Rid = Rid
        self.GameID = GameID
        self.ZoneID = ZoneID
        
    def __repr__(self): 
        
        return '<GameListtoArea: Rid="%s", GameID="%s", ZoneID="%s">' % (self.Rid, self.GameID, self.ZoneID)
    
class GameGroupRelation(declarativeBase):
    __tablename__ = 'gamegrouprelation'
    __table_args__ = (UniqueConstraint('GameID', 'GroupID', name='GameID_GroupID_UK'), )
    
    # Column
    Rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    GameID = Column(Integer, nullable=False, default=0)  
    
    GroupID = Column(Integer, nullable=False, default=0)  
    
    def __init__(self, Rid, GameID, GroupID):
        self.Rid = Rid
        self.GameID = GameID
        self.GroupID = GroupID
        
    def __repr__(self):

        return '<GameGroupRelation: Rid="%s", GameID="%s", GroupID="%s">' % (self.Rid, self.GameID, self.GroupID)