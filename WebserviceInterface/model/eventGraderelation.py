# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['EventGradeRelation']

class EventGradeRelation(declarativeBase):
    __tablename__ = 'eventgraderelation'
    
    # Columns
    grade = Column(Integer, primary_key=True, nullable=False) 
    
    oc = Column(Integer, nullable=False, default=0)
    
    mail = Column(Integer, nullable=False, default=0)
    
    smcd = Column(Integer, nullable=False, default=0)
    
    def __init__(self, grade, oc, mail, smcd):
        self.grade = grade
        self.oc = oc
        self.mail = mail
        self.smcd = smcd
        
    def __repr__(self):
        
        return '<EventGradeRelation: grade="%s", oc="%s", mail="%s", smcd="%s">' % (self.grade, self.oc, self.mail, self.smcd)
    
    