# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import hashlib
from model.aduser import ADuser
from model import DBSession, metadata, declarative_base

class addUser:
    
    def __init__(self, name='Interface'):
        
        self.name = name
        self.username = ''
        self.password = ''
        self.validateTime = ''
        
    def AddLocaluser(self, username='anonymous', password='', validateTime='00000000000'): 
        
        self.username = username
        self.password = self.createUserPassword(self.name, self.username, password) 
        self.validateTime = validateTime

        checkCount = len(DBSession.query(ADuser).all())

        try:       
            checkExist = DBSession.query(ADuser).filter_by(username = self.username).first()

            if checkExist.password == self.password:
                checkExist.validateTime = self.validateTime
            else:
                DBSession.delete(checkExist)
                DBSession.add(ADuser(int(checkCount)+1, self.username, self.password, self.validateTime))
        except:
            DBSession.add(ADuser(int(checkCount)+1, self.username, self.password, self.validateTime))
        
        finally:
            DBSession.commit()   
    
    def createUserPassword(self, jam, username, password):
        
        hashcreate = hashlib.sha1()
        
        secretPassword = jam+password+username
        
        hashcreate.update(secretPassword)
        
        hashValue = hashcreate.hexdigest()
        
        return hashValue