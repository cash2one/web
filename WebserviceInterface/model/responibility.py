# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text, BIGINT
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index
from sqlalchemy import UniqueConstraint

__all__ = ['ResponibilityRelation', 'ResponibilityGroup', 'ResonibilityUser']

class ResponibilityRelation(declarativeBase):
    __tablename__ = 'responibilityrelation'
    __table_args__ = (UniqueConstraint('TemplateID', 'gid', name='TemplateID_gid_UK'), )
    
    # Columns
    Rid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    TemplateID = Column(Integer, nullable=False)
    
    gid = Column(Integer, nullable=False)
    
    def __init__(self, Rid, TemplateID, gid):
        self.Rid = Rid
        self.TemplateID = TemplateID
        self.gid = gid
        
    def __repr__(self):
        
        return '<ResponibilityRelation: Rid="%s", TemplateID="%s", gid="%s">' % (self.Rid, self.TemplateID, self.gid)
    
class ResponibilityGroup(declarativeBase):
    __tablename__ = 'responibilitygroup'
    
    # Column 
    gid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    Name = Column(String(256), nullable=False, default=u'')
    
    Desc = Column(String(256), nullable=False, default=u'')
    
    def __init__(self, gid, Name, Desc):
        self.gid = gid
        self.Name = Name
        self.Desc = Desc
        
    def __repr__(self):
        
        return '<ResponibilityGroup: gid="%s", Name="%s", Desc="%s">' % (self.gid, self.Name, self.Desc)
    
class ResonibilityUser(declarativeBase):
    __tablename__ = 'resonibilityuser'
    __table_args__ = (UniqueConstraint('gid', 'username', name='gid_username_UK'), )
    
    # Columns
    uid = Column(Integer, primary_key=True, nullable=False, default=0)
    
    gid = Column(Integer, nullable=False, default=0)
    
    username = Column(String(100), nullable=False, default=u'')
    
    userPYname = Column(String(100), nullable=False, default=u'')
    
    smcd = Column(BIGINT, nullable=False, default=0)
    
    mail = Column(String(100), nullable=False, default=u'')
    
    oc = Column(String(100), nullable=False, default=u'')
    
    note = Column(Text, nullable=False)
    
    important = Column(String(100), nullable=False, default=u'False')
    
    def __init__(self, uid, gid, username, userPYname, smcd, mail, oc, note, important):
        self.uid = uid
        self.gid = gid
        self.username = username
        self.userPYname = userPYname
        self.smcd = smcd
        self.mail = mail
        self.oc = oc
        self.note = note
        self.important = important
        
    def __repr__(self):
        
        return '<ResonibilityUser: uid="%s", gid="%s", username="%s", userPYname="%s", smcd="%s", mail="%s", oc="%s", note="%s", important="%s">' % (self.uid, self.gid, self.username, self.userPYname, self.smcd, self.mail, self.oc, self.note, self.important)