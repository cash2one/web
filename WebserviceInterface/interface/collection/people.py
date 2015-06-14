# -*- coding: utf-8 -*-
''' 
@author : majian
This module is linked with people curves
read from url : view-source:http://identification.ztgame.com/identification/interface.php?op=GetSysParam&app%20code=monitor
'''

import os, re 
import MySQLdb
import urllib2
import time
import chardet

from ServiceConfig.config import readFromConfigFile
from model.dbsearch import LogicSearch, DataSearch
from ServiceConfig.urlexplain import Urlex
from timeCalc import TimePass
from dbconnect import Connect

from model import metadata, DBSession, declarativeBase
from model.gamename import Gameinform
from interface.collection.flushtables import FlushGameName

class NumberofPeople:
    
    def __init__(self):
        
        self.username = ""
        self.password = ""
        self.nowtime = "" 
        self.getDay = ""
        self.dbfileName = ""
        self.searchTime = ""
        self.timeList = []
        self.Resource = {}    
        self.returns = {} 
    
    def Controller(self, gameName, timePass):
        
        # Part A : get Project Name
        # Ensure the game exist 
        # get information about game detail
        # from url about the platform
        if gameName.upper() == 'ALL':
            self.Resource = Urlex().getInformationMultiple(gameName)
            for key,value in self.Resource.items():
                tmpDict={}
                tmpDict[key]=value
                
                tmpRESULT = self.ControlOperation(gameName, timePass, tmpDict)
		
		print "######### NAME, tmpRESULT:", key, tmpRESULT
                self.returns[key]=tmpRESULT
                self.returns['Status'] = 'Success'
        else:
            '''
            example: {'DoDo': {'username': 'y6ffpsEk', 'password': '3j4JPrFYOBlN', 'ipaddress': '192.168.100.171', 'dbname': 'InfoServer_DoDo', 'port': 3315}}
            '''
            self.Resource = Urlex().getInformationSingle(gameName)
            self.returns[gameName] = self.ControlOperation(gameName, timePass, self.Resource)
            self.returns['Status'] = 'Success'
            
        return self.returns    
               
    def ControlOperation(self, gameName, timePass, SingleResource):
        
        getSearchResult = {}
        # Part B: get collection time
        # self.searchTime is the new search time
        parttime = TimePass().getNowtime()
 
        self.dbfileName = TimePass().getDBfilename(parttime['timeStamp'])
        
        for key,value in SingleResource.items():
            try:
                # create connect
                (conn, cursor) = Connect().create(value)
                
                sql='select * from %s order by rTimestamp desc limit 0,1' % (self.dbfileName)
                cursor.execute(sql)
                result=cursor.fetchall()
                for eachresult in result:
                    self.searchTime = eachresult[1]
        
                # drop connect
                Connect().drop(conn, cursor)
                
            except Exception, e:
                return 'Could not found %s' % self.dbfileName
        
        # Part c :  get timePass and get the timestamp
        # calcuate time pass
        # format : {'timeStamp': 1361179903, 'timeList': [1361179903L, 1361179843L, 1361179783L, 1361179723L, 1361179663L, 1361179603L]}
        getTime = TimePass().TimeCalcuate(timePass, self.searchTime)
        self.timeList = getTime['timeList']
        self.nowtime = int(getTime['timeStamp'])
           
           
        # Part d : part list and collect
        # give it to different part     
        ''' 
        example - 'ZTQY': {'username': 'NDa1fxyv', 'password': 'iPQlacpVxeUr', 'ipaddress': '192.168.100.81', 'port': '3313', 'dbname': 'InfoServer_ZTQY'}
        '''   
        
        for key,value in SingleResource.items():
            
            for eachTimes in self.timeList:
                try:
                    # create connect with database
                    (tryconn, trycursor) = Connect().create(value)
                    
                    sql='select * from %s where rTimestamp=%s' % (self.dbfileName, eachTimes)
                    trycursor.execute(sql)
                    result=trycursor.fetchall()
                    
                    TempArrayforZone=[]
                    TempArrayforrealOnline=[]
                    for eachline in result:
                    # DB struct : NO rTimestamp ServerType ServerID GameZone ZoneName OnlineNum realOnlineNum
                        (searchNo, rTimestamp, ServerType, ServerID, GameZone, ZoneName, OnlineNum, realOnlineNum) = eachline[0],eachline[1],eachline[2],eachline[3],eachline[4],eachline[5],eachline[6],eachline[7]

                        TempArrayforZone.append(GameZone)
                        TempArrayforrealOnline.append(realOnlineNum)
           
        # Part e: select all need for fill into new dictionary
        # Return format is : GameZoneid: [1min, 2min, 3min, 4min, 5min], next...
        # the result dictionary like : 720897L: [22234L, 22193L, 22179L, 22131L, 22107L], 721898L: [20500L, 20453L, 20390L, 20339L, 20294L] .....         
                    if len(getSearchResult) == 0:
                        for eachi in range(len(TempArrayforZone)):
                                getSearchResult[TempArrayforZone[eachi]] = []
                    else:
                        for eachi in range(len(TempArrayforZone)):
                            getSearchResult[TempArrayforZone[eachi]].append(TempArrayforrealOnline[eachi])
                    
                        
                    Connect().drop(tryconn, trycursor)
                    
                except Exception, e:
                    return 'Could not part of result and close connect with database'
                
        return getSearchResult 



class RealofPeople:
    
    def __init__(self):
        
        self.username = ""
        self.password = ""
        self.nowtime = "" 
        self.getDay = ""
        self.dbfileName = ""
        self.searchTime = ""
        self.timeList = []
        self.Resource = {}    
        self.returns = {} 
    
    def RealController(self, gameName, timePass):
        
        # Part A : get Project Name
        # Ensure the game exist 
        # get information about game detail
        # from url about the platform
        if gameName.upper() == 'ALL':
            self.Resource = Urlex().getInformationMultiple(gameName)
            for key,value in self.Resource.items():
                tmpDict={}
                tmpDict[key]=value
                
                tmpRESULT = self.RealControlOperation(gameName, timePass, tmpDict)
                self.returns[key]=tmpRESULT
                self.returns['Status'] = 'Success'
        else:
            '''
            example: {'DoDo': {'username': 'y6ffpsEk', 'password': '3j4JPrFYOBlN', 'ipaddress': '192.168.100.171', 'dbname': 'InfoServer_DoDo', 'port': 3315}}
            '''
            self.Resource = Urlex().getInformationSingle(gameName)
            self.returns[gameName] = self.RealControlOperation(gameName, timePass, self.Resource)
            self.returns['Status'] = 'Success'
         
        return self.returns    
               
    def RealControlOperation(self, gameName, timePass, SingleResource):
        
        getRealResult = {}
        # Part B: get collection time
        # self.searchTime is the new search time
        parttime = TimePass().getNowtime()
 
        self.dbfileName = TimePass().getDBfilename(parttime['timeStamp'])
        
        for key,value in SingleResource.items():
            try:
                # create connect
                (conn, cursor) = Connect().create(value)
                
                sql='select * from %s order by rTimestamp desc limit 0,1' % (self.dbfileName)
                cursor.execute(sql)
                result=cursor.fetchall()
                for eachresult in result:
                    self.searchTime = eachresult[1]
        
                # drop connect
                Connect().drop(conn, cursor)
                
            except Exception, e:
                return 'Could not found %s' % self.dbfileName
        
        # Part c :  get timePass and get the timestamp
        # calcuate time pass
        # format : {'timeStamp': 1361179903, 'timeList': [1361179903L, 1361179843L, 1361179783L, 1361179723L, 1361179663L, 1361179603L]}
        getTime = TimePass().TimeCalcuate(timePass, self.searchTime)
        self.timeList = getTime['timeList']
        self.nowtime = int(getTime['timeStamp'])
           
           
        # Part d : part list and collect
        # give it to different part     
        ''' 
        example - 'ZTQY': {'username': 'NDa1fxyv', 'password': 'iPQlacpVxeUr', 'ipaddress': '192.168.100.81', 'port': '3313', 'dbname': 'InfoServer_ZTQY'}
        '''   
        
        for key,value in SingleResource.items():
            
            for eachTimes in self.timeList:
                try:
                    # create connect with database
                    (tryconn, trycursor) = Connect().create(value)
                    
                    sql='select * from %s where rTimestamp=%s' % (self.dbfileName, eachTimes)
                    trycursor.execute(sql)
                    result=trycursor.fetchall()
                    
                    TempArrayforZone=[]
                    TempArrayforrealOnline=[]
                    
                    for eachline in result:
                    # DB struct : NO rTimestamp ServerType ServerID GameZone ZoneName OnlineNum realOnlineNum
                        (searchNo, rTimestamp, ServerType, ServerID, GameZone, ZoneName, OnlineNum, realOnlineNum) = eachline[0],eachline[1],eachline[2],eachline[3],eachline[4],eachline[5],eachline[6],eachline[7]
                        
#                        test ok part
#                        if type(ZoneName).__name__ != 'unicode':
#                            ZoneName = unicode(ZoneName, 'GB2312')
#                            newZoneName = ZoneName.decode('utf-8')
#                        else:
#                            newZoneName=ZoneName.decode('utf-8')

                        
                        if chardet.detect(ZoneName)['encoding'] == 'utf-8':
                            newZoneName = ZoneName 
                        elif chardet.detect(ZoneName)['encoding'] == 'windows-1252':
                            ZoneName = unicode(ZoneName,'cp1252')
                            newZoneName = ZoneName.decode('utf-8') 
                        else:
                            try:
                                ZoneName = unicode(ZoneName, 'GB2312')
                            except:
                                ZoneName = unicode(ZoneName, 'GBK')
                                if re.search(r'屌丝传奇', ZoneName):
                                    ZoneName = 'DSCQ'
                            newZoneName = ZoneName.decode('utf-8')

                        TempArrayforZone.append(newZoneName)
                        if OnlineNum:
                            TempArrayforrealOnline.append(OnlineNum)
                        else:
                            TempArrayforrealOnline.append('None')    
           
        # Part e: select all need for fill into new dictionary
        # Return format is : GameZoneid: [1min, 2min, 3min, 4min, 5min], next...
        # the result dictionary like : 720897L: [22234L, 22193L, 22179L, 22131L, 22107L], 721898L: [20500L, 20453L, 20390L, 20339L, 20294L] .....      
 
                    if len(getRealResult) == 0:
                        for eachi in range(len(TempArrayforZone)):
                                getRealResult[TempArrayforZone[eachi]] = []
                    else:
                        for eachi in range(len(TempArrayforZone)):
                            getRealResult[TempArrayforZone[eachi]].append(TempArrayforrealOnline[eachi])
     
                    Connect().drop(tryconn, trycursor)
                    
                except Exception, e:
                    #return 'Could not part of result and close connect with database'
                    return str(e)

        for pk, pv in getRealResult.items():
            if 'None' not in pv:
                if len(pv) != 0:
                    Variable = int(int(len(pv)) / 5)
                    if Variable == 2:
                        tmpPV=[]
                        tmpPV.append(int(pv[0]+pv[1]))
                        tmpPV.append(int(pv[2]+pv[3]))
                        tmpPV.append(int(pv[4]+pv[5]))
                        tmpPV.append(int(pv[6]+pv[7]))
                        tmpPV.append(int(pv[8]+pv[9]))
                        getRealResult[pk] = tmpPV
                    elif Variable == 3:
                        tmpPV=[]
                        tmpPV.append(int(pv[0]+pv[1]+pv[2]))
                        tmpPV.append(int(pv[3]+pv[4]+pv[5]))
                        tmpPV.append(int(pv[6]+pv[7]+pv[8]))
                        tmpPV.append(int(pv[9]+pv[10]+pv[11]))
                        tmpPV.append(int(pv[12]+pv[13]+pv[14]))
                        getRealResult[pk] = tmpPV
            # This else will be used in not search any of game curves 
            # and will be change to get online user number  
            # else       
             
        return getRealResult   
'''
This Methos is used to select Now data of Number Curves
'''
class NowofCurves:
    
    def __init__(self):
        
        self.returns = {}
        
    def nowController(self, gameName):
        
        ''' No.1 : Clear project information and flush of local database'''
        FlushGameName().getFlushoftable('ALL')
            
        ''' No.2 : examine input '''
        searchResult = DataSearch().sureGameNameinTable(gameName)
        if searchResult == 'success':
            getReturnofPeople = RealofPeople().RealController(gameName, 1)
            if getReturnofPeople['Status'] == 'Success':
                for key,value in getReturnofPeople.items():
                    if key != 'Status':
                            
                        for k,v in value.items():
                            print "#### key, value", key, value
                            #k=unicode(k,'GB2312')
                            #k=k.decode('utf-8')
                            self.returns[k]=v[0]
                      
            else:
                return getReturnofPeople
        else:
            return searchResult

        return self.returns
''' 
This Method is used to select History Data of Number Curves
'''
class HistoryofCurves:
    
    def __init__(self):
        
        self.dbfileName = ""
        self.history = {}
        self.Resource = {}    
        self.returns = {}
        
    def historyController(self, gameName, timestamp):
        
        ''' No.1 judge of two input variable '''
        if gameName.upper() == 'ALL' or gameName.upper() == 'NONE':
            return 'Call Method variable ERROR: gameName : %s' % gameName
        
        if type(timestamp).__name__ != 'int' or len(str(timestamp)) != 10:
            return 'Call Method variable ERROR: timestamp not integer or length not fillin.'
        
        ''' No.2 get each game defail like:
        example : {'DoDo': {'username': 'y6ffpsEk', 'password': '3j4JPrFYOBlN', 'ipaddress': '192.168.100.171', 'dbname': 'InfoServer_DoDo', 'port': 3315}}
        '''
        self.Resource = Urlex().getInformationSingle(gameName)
        self.returns = self.historyControlOperation(gameName, timestamp, self.Resource)
        self.returns['Status']='Success'
        return self.returns
        
    
    def historyControlOperation(self, gameName, timestamp, SingleResource):
        
        ''' No.3  Sure Datafile exist and get the last one Record '''
        tmpSDict = {} 
        self.dbfileName = TimePass().getDBfilename(timestamp)

        for key,value in SingleResource.items():
            try:
                # create connect
                (conn, cursor) = Connect().create(value)
                
                sql_table='select * from %s' % self.dbfileName 
                sql_like=' where rTimestamp like'+" \"%"+str(timestamp)[0:8]+"%\""
                sql = sql_table+sql_like
                cursor.execute(sql)
                result=cursor.fetchall()
                
                for eachresult in result:
                    tmpName=unicode(eachresult[5],'GB2312')
                    tmpName=tmpName.decode('utf-8')
                    tmpSDict[tmpName]=eachresult[7]  
    
                # drop connect
                Connect().drop(conn, cursor)
                
                self.returns[key]=tmpSDict
                
            except Exception, e:
                msg = 'Could not found %s' % self.dbfileName
                self.returns[key]=msg
    
        return self.returns
