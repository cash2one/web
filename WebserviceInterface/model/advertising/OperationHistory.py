# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model.__cmdbinit__ import cmetadata, CMDBSession, cmdeclarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean, Text
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['OperationHistory']

class OperationHistory(cmdeclarativeBase):
    __tablename__ = 'operationhistory'
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    CurrentTimestamp = Column(Integer, nullable=False, default=0)
    
    opUsername = Column(String(100), nullable=False, default=u'None')
    
    Content = Column(Text, nullable=False, default='')
    
    Status = Column(Integer, nullable=False, default=0)
    
    def __init__(self, CurrentTimestamp, opUsername, Content, Status, id=0):
        self.id = id
        self.CurrentTimestamp = CurrentTimestamp
        self.opUsername = opUsername
        self.Content = Content
        self.Status = Status
        
    def __repr__(self):
        
        return '<OperationHistory: id="%s", CurrentTimestamp="%s", opUsername="%s", Content="%s", Status="%s">' % (self.id, self.CurrentTimestamp, self.opUsername, self.Content, self.Status)
    