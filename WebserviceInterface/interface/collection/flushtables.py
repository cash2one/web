# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re 
import urllib2
import time

from model import metadata, DBSession, declarativeBase

from ServiceConfig.urlexplain import Urlex
from ServiceConfig.config import readFromConfigFile
from model.gamename import Gameinform
from model.gamelist import GameList
from interface.collection.dbconnect import Connect

''' 
This Method used to clear and flush new project information in local database
about id, gameName, host, port, dbname in all 5 items 
'''    
class FlushGameName:
    
    def __init__(self):
        
        self.flush = ""
        self.count = 0
        
    def getFlushoftable(self, signal='ALL'):
        
        # No.1 clear table of gamename
        localGameName = DBSession.query(Gameinform).all()
        
        if len(localGameName) != 0:
            for eachGamename in range(len(localGameName)):
                DBSession.delete(localGameName[eachGamename])
        
        DBSession.commit()
       
        # No.2 get each Game information & fill in table
       
        self.flush = Urlex().getInformationMultiple(signal)
    
        for key,value in self.flush.items():
            if key != 'NULL':
                DBSession.add(Gameinform(self.count, key, value['ipaddress'], value['port'], value['dbname']))
                self.count += 1

        DBSession.commit()
        
class FlushGameList:
    
    def __init__(self):
        
        self.flush = ""
        self.count = 0
        self.getConfig = {}
        self.change = {}
        
    def FlushofGamelist(self):
        
        ''' No.1 clear table of gamelist '''
        localgamelist = DBSession.query(GameList).all()
        
        if len(localgamelist) != 0:
            for eachlist in range(len(localgamelist)):
                DBSession.delete(localgamelist[eachlist])
                
        DBSession.commit()
        
        ''' No.2 analyst Config and create conn '''
        self.getConfig = readFromConfigFile().get_config_zonelist('/WebserviceInterface/ServiceConfig/setting.ini')
        
        for eachTuple in range(len(self.getConfig['Zonelist'])):
            if self.getConfig['Zonelist'][eachTuple][0] == 'username':
                self.change['username'] = self.getConfig['Zonelist'][eachTuple][1]
            elif self.getConfig['Zonelist'][eachTuple][0] == 'password':
                self.change['password'] = self.getConfig['Zonelist'][eachTuple][1]
            elif self.getConfig['Zonelist'][eachTuple][0] == 'ipaddress':
                self.change['ipaddress'] = self.getConfig['Zonelist'][eachTuple][1]
            elif self.getConfig['Zonelist'][eachTuple][0] == 'port':
                self.change['port'] = int(self.getConfig['Zonelist'][eachTuple][1])
            elif self.getConfig['Zonelist'][eachTuple][0] == 'dbname':
                self.change['dbname'] = self.getConfig['Zonelist'][eachTuple][1]
            elif self.getConfig['Zonelist'][eachTuple][0] == 'tablename':
                self.change['tablename'] = self.getConfig['Zonelist'][eachTuple][1]
        
        (conn, cursor) = Connect().create(self.change)
        
        sql = 'select * from %s' % self.change['tablename']
        cursor.execute(sql)
        result=cursor.fetchall()
        for i in result:
            print i
