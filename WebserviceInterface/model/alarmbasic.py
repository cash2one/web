# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['AlarmUser', 'AlarmGroup']

class AlarmUser(declarativeBase):
    __tablename__ = 'alarmuser'
    
    # Column 
    userID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    userName = Column(String(100), nullable=False, default=u'')
    
    userStatus = Column(Integer, nullable=False, default=0)
    
    OC = Column(String(100), nullable=False, default=0)
    
    SMCD = Column(String(100), nullable=False, default=0)
    
    MAIL = Column(String(100), nullable=False, default=0)
    
    def __init__(self, userID, userName, userStatus, OC, SMCD, MAIL):
        self.userID = userID
        self.userName = userName
        self.userStatus = userStatus
        self.OC = OC
        self.SMCD = SMCD
        self.MAIL = MAIL
        
    def __repr__(self):
        
        return '<AlarmUser: userID="%s", userName="%s", userStatus="%s", OC="%s", SMCD="%s", MAIL="%s">' % (self.userID, self.userName, self.userStatus, self.OC, self.SMCD, self.MAIL)

class AlarmGroup(declarativeBase):
    __tablename__ = 'alarmgroup'
    
    # Column
    groupID = Column(Integer, primary_key=True, nullable=False, default=0)
    
    groupName = Column(String(100), nullable=False, default=u'')
    
    groupBelong = Column(Integer, nullable=False, default=1)
    
    groupStatus = Column(Integer, nullable=False, default=0)
    
    def __init__(self, groupID, groupName, groupBelong, groupStatus):
        self.groupID = groupID
        self.groupName = groupName
        self.groupBelong = groupBelong
        self.groupStatus = groupStatus
        
    def __repr__(self):
        
        return '<AlarmGroup: groupID="%s", groupName="%s", groupBelong="%s", groupStatus="%s">' % (self.groupID, self.groupName, self.groupBelong, self.groupStatus)