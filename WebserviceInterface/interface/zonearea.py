# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import chardet

from ServiceConfig.config import readFromConfigFile
from interface.collection.dbconnect import Connect
from BaseClass.timeBasic import TimeBasic

class ZoneListPlatformInterface:
    
    def __init__(self):
        
        self.username = ''
        self.password = ''
        self.ipaddress = ''
        self.dbname = ''
        self.port = ''
        self.dblinkDict = {}
        self.zonebygame = []
        
        analystConfig = readFromConfigFile()
        getAnalyst = analystConfig.get_config_zonelist('/WebserviceInterface/ServiceConfig/setting.ini')
        
        for key,value in getAnalyst.items():
            if key == 'Zonelist':
                for eachvalue in value:
                    if eachvalue[0] == 'username':
                        self.username = eachvalue[1]
                    elif eachvalue[0] == 'password':
                        self.password = eachvalue[1]
                    elif eachvalue[0] == 'ipaddress':
                        self.ipaddress = eachvalue[1]
                    elif eachvalue[0] == 'port':
                        self.port = eachvalue[1]
                    elif eachvalue[0] == 'dbname':
                        self.dbname = eachvalue[1]
                        
        self.dblinkDict = dict(username=self.username, password=self.password, ipaddress=self.ipaddress, port=int(self.port), dbname=self.dbname)

    ''' From GameID to search ZoneID '''
    def GametoZone(self, GameID):
        
        try:
            ''' Step 1. Link with database '''
            (Zconnect, Zcursor) = Connect().createwithUtf8(self.dblinkDict)
        
            ''' Step 2. decide table name '''
            nowtime = int(round(time.time()))
            timefmt = TimeBasic().timeControl(nowtime, 4)
            tablename = "zoneInfo_%s" % (timefmt)
        
            ''' Step 3. search data in zoneinfo '''
            cmd = 'select * from %s where game=%s' % (tablename, GameID)
            Zcursor.execute(cmd)
            result = Zcursor.fetchall()
            
            for eachline in result:
                tmpDict = {}
                tmpDict = dict(ZoneID=eachline[1], zone_name=eachline[2], zone_desc=eachline[3])
                self.zonebygame.append(tmpDict)
            
            ''' Step 4. close connection '''
            Connect().drop(Zconnect, Zcursor)
            
            if len(self.zonebygame) != 0:
                return dict(Status='Success', ZoneList=self.zonebygame)
            else:
                msg='MySQL could not found any Data in zoneInfo by GameID=%s' % GameID
                return dict(Status='False', msg=msg)
                
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
    ''' From GameID and zoneID get zonedetail '''
    def zonedetail(self, GameID, ZoneID):
        
        try:
            ''' Step 1. Link with database '''
            (Dconnect, Dcursor) = Connect().createwithUtf8(self.dblinkDict)
            
            ''' Step 2. decide table name '''
            nowtime = int(round(time.time()))
            timefmt = TimeBasic().timeControl(nowtime, 4)
            tablename = "zoneInfo_%s" % (timefmt)
            
            ''' Step 3. search data in zoneinfo '''
            cmd = 'select * from %s where game=%s and zone=%s' % (tablename, GameID, ZoneID)
            Dcursor.execute(cmd)
            result = Dcursor.fetchone()
            
            if result:
                detail = dict(zoneName=result[2], zoneDesc=result[3])
                return dict(Status='Success', detail=detail)

            else:
                msg='MySQL could not found zoneinformation in zoneInfo by GameID=%s & ZoneID=%s.' % (GameID, ZoneID)
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            return dict(Status='False', msg=str(e))
