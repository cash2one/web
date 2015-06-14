# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from ServiceConfig.config import readFromConfigFile
from interface.collection.dbconnect import Connect

class StoreinMainServer:
    
    def __init__(self):
        
        self.returns = ""
        self.username = ""
        self.password = ""
        self.ipaddress = ""
        self.port = ""
        self.dbname = ""
        
        self.iusername = ""
        self.iip = ""
        self.iport = ""
        self.ipassword = ""
        self.idbname = ""
        
        getConfig = readFromConfigFile().get_config_mainserver()
        getConfigofdatabase = readFromConfigFile().get_config_sqlalchemy()
        
        for key,value in getConfig.items():
            if key == 'MainServer':
                for eachElement in value:
                    if eachElement[0] == 'username':
                        self.username = eachElement[1]
                    elif eachElement[0] == 'ip':
                        self.ipaddress = eachElement[1]
                    elif eachElement[0] == 'port':
                        self.port = eachElement[1] 
                    elif eachElement[0] == 'password':
                        self.password = eachElement[1]
                    elif eachElement[0] == 'dbname':    
                        self.dbname = eachElement[1]
        
        for keys,values in getConfigofdatabase.items():
            if keys == 'database':
                for eachElement in values:
                    if eachElement[0] == 'username':
                        self.iusername = eachElement[1]
                    elif eachElement[0] == 'password':
                        self.ipassword = eachElement[1]
                    elif eachElement[0] == 'ip':
                        self.iip = eachElement[1]
                    elif eachElement[0] == 'port':
                        self.iport = eachElement[1]
                
        self.interConnectDict = dict(username=self.iusername, password=self.ipassword, ipaddress=self.iip, port=int(self.iport), dbname='interDB')           
        self.ConnectionDict = dict(username=self.username, password=self.password, ipaddress=self.ipaddress, port=int(self.port), dbname=self.dbname)
        
    def getTestofMainServer(self):
        
        try:
            getReturnConnect = Connect().TestConnect(self.ConnectionDict)
            
            if getReturnConnect['Status'] != 'Success':
                return getReturnConnect
  
        except Exception, e:
            return dict(Status='False', msg=str(e))
        
        return dict(Status='Success')
    
    def checkTableExistinMainServer(self, list):
        
        searchTablelist = []
        
        try:
            (TableConn, TableCursor) = Connect().createwithSYS(self.ConnectionDict)
            
            cmd = "SELECT TABLE_NAME, TABLE_TYPE from TABLES where TABLE_SCHEMA='%s'" % self.dbname
            TableCursor.execute(cmd)
            result = TableCursor.fetchall()
            
            for eachline in result:
                searchTablelist.append(eachline[0])

            getCmp = set(list)&set(searchTablelist)
            if len(getCmp) == len(list):
                Connect().drop(TableConn, TableCursor)
                return dict(Status='Success')
            else:
                Connect().drop(TableConn, TableCursor)
                return dict(Status='False',msg='Table not Exist. Please Check.')
            
        except Exception, e:
            Connect().drop(TableConn, TableCursor)
            return dict(Status='False', msg=str(e)) 
        
    def insertintotable(self, TableName, ParmContent):
        
        ColumnList = []
        
        try:
            ''' Step 1. link with MainServer '''
            (MConn, MCursor) = Connect().createwithSYS(self.ConnectionDict)

            ''' Step 2. analyst Columns '''
            cmd = "SELECT TABLE_NAME, COLUMN_NAME, COLUMN_DEFAULT, IS_NULLABLE from COLUMNS where TABLE_SCHEMA = '%s' and TABLE_NAME='%s'" % (self.dbname, TableName)
            MCursor.execute(cmd)
            result = MCursor.fetchall()
            
            for eachline in result:
                ColumnList.append(eachline[1])
                
            ''' Step 3. check input Column Count '''
            if len(ParmContent) != len(ColumnList):
                return dict(Status='False', msg='input Variable Error. Count Not Right.')

            ''' Step 4. Create new Connection '''
            (Tconn, Tcursor) = Connect().createwithUtf8(self.ConnectionDict)
            
            ''' Step 5. new insert cmd create '''
            #TableName, ColumnList, ParmContent
            newColumnString = ','.join(ColumnList)
            newParmContent = ','.join(ParmContent)
            
            newCmd = 'INSERT INTO %s (%s) values(%s)' % (TableName, newColumnString, newParmContent)
            Tcursor.execute(newCmd)
            
            ''' Step Finally. drop with information_schema and monitor. '''
            Connect().drop(MConn, MCursor)
            Connect().drop(Tconn, Tcursor)
            
            return dict(Status='Success')
                
        except Exception, e:
            Connect().drop(MConn, MCursor)
            Connect().drop(Tconn, Tcursor)
            return dict(Status='False', msg=str(e)) 
        
    def searchtablemaxline(self, tableName):
        
        try:
            (MaxConn, Maxcursor) = Connect().createwithUtf8(self.interConnectDict)
            
            cmd = 'select count(*) from %s' % tableName
            Maxcursor.execute(cmd)
            result = Maxcursor.fetchone()
            
            Count = result[0]
            if Count and Count > 0:
                return dict(Status='Success', Count=Count)
            else:
                msg = 'Could not found table : %s Count.' % tableName
                return dict(Status='False', msg=msg)
            
        except Exception, e:
            return dict(Status='False', msg=str(e))