# -*- coding: utf-8 -*-
''' @author : majian'''

import os
import sys
from model import metadata, DBSession, declarativeBase
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relation, synonym
from sqlalchemy.schema import Index

__all__ = ['Packtype', 'Validate', 'Compress', 'Encrypt']

class Packtype(declarativeBase): 
    __tablename__ = 'packtype_compress_encrypt'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    packtype = Column(Integer, nullable=False, default=0)
    
    compress = Column(Integer, nullable=False, default=0)
    
    encrypt = Column(Integer, nullable=False, default=0)
    
    validate = Column(Integer, nullable=False, default=0)
    
    def __init__(self, id, packtype, compress, encrypt, validate):
        
        self.id = id
        self.packtype = packtype
        self.compress = compress
        self.encrypt = encrypt
        self.validate = validate
        
        
    def __repr__(self):
        
        return '<Packtype: id="%s", packtype="%s", compress="%s", encrypt="%s", validate="%s">' % (self.id, self.packtype, self.compress, self.encrypt, self.validate)
    
class Validate(declarativeBase):
    __tablename__ = 'validation'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    vname = Column(String(10), nullable=False, default=u'')
    
    def __init__(self, id, vname):
        
        self.id = id
        self.vname = vname
        
    def __repr__(self):
        
        return '<Validate: id="%s", vname="%s">' % (self.id, self.vname)

class Compress(declarativeBase):
    __tablename__ = 'compress'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    compressID = Column(Integer, nullable=False, default=0)
    
    compressDesc = Column(String(256), nullable=False, default=u'')
    
    def __init__(self, id, compressID, compressDesc):
        
        self.id = id
        self.compressID = compressID
        self.compressDesc = compressDesc
        
    def __repr__(self):
        
        return '<Compress: id="%s", compressID="%s", compressDesc="%s">' % (self.id, self.compressID, self.compressDesc)
    
class Encrypt(declarativeBase):
    __tablename__ = 'encrypt'
    
    # Columns
    id = Column(Integer, primary_key=True, nullable=False, default=0)
    
    encryptID = Column(Integer, nullable=False, default=0)
    
    encryptDesc = Column(String(256), nullable=False, default=u'')
    
    def __init__(self, id, encryptID, encryptDesc):
        
        self.id = id
        self.encryptID = encryptID
        self.encryptDesc = encryptDesc
        
    def __repr__(self):
        
        return '<Encrypt: id="%s", encryptID="%s", encryptDesc="%s">' % (self.id, self.encryptID, self.encryptDesc)