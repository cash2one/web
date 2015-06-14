# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import MySQLdb
import time

class Connect:
    
    def __init__(self):
        
        self.connect = ""
        self.cursor = ""
        self.connectutf8 = ""
        self.cursorutf8 = ""
        self.connectsys = ""
        self.cursorsys = ""
        self.testconnect = ""
    
    def create(self, Dict):
        
        self.connect = MySQLdb.connect(host=Dict['ipaddress'],
                                          user=Dict['username'],
                                          passwd=Dict['password'],
                                          port=Dict['port'],
                                          db=Dict['dbname'])
        self.cursor = self.connect.cursor()
        
        return (self.connect, self.cursor)
    
    def createwithUtf8(self, Dict):
        
        self.connectutf8 = MySQLdb.connect(host=Dict['ipaddress'],
                                          user=Dict['username'],
                                          passwd=Dict['password'],
                                          port=Dict['port'],
                                          db=Dict['dbname'],
                                          charset='utf8')
        self.cursorutf8 = self.connectutf8.cursor()
        
        return (self.connectutf8, self.cursorutf8)
    
    def createwithSYS(self, Dict):
        
        self.connectsys = MySQLdb.connect(host=Dict['ipaddress'],
                                          user=Dict['username'],
                                          passwd=Dict['password'],
                                          port=Dict['port'],
                                          db='information_schema')
        self.cursorsys = self.connectsys.cursor()
        
        return (self.connectsys, self.cursorsys)
    
    def TestConnect(self, Dict):
        
        try:
            
            self.testconnect = MySQLdb.connect(host=Dict['ipaddress'],
                                          user=Dict['username'],
                                          passwd=Dict['password'],
                                          port=Dict['port'],
                                          db=Dict['dbname'])
            
            return dict(Status='Success')

        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    def drop(self, privateconn, privatecur):
        
        privatecur.close()
        privateconn.close()
        
        return "success"