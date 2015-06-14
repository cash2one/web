# -*- coding: utf-8 -*-
''' @author : majian'''

import sys
import sqlalchemy
import pyodbc
from sqlalchemy import *

reload(sys)
sys.setdefaultencoding('utf8')

from ServiceConfig.config import readFromConfigFile

class ConnectAMT:
    
    def __init__(self):
        
        self.dbtype = ""
        self.username = ""
        self.password = ""
        self.ipaddress = ""
        self.port = ""
        self.dbname = ""
        self.charset = ""
        self.project = ""
        
        getReturn = readFromConfigFile().get_config_giantAMT()
        for eachline in getReturn['AMT']:
            if eachline[0] == 'dbtype':
                self.dbtype = eachline[1]
            elif eachline[0] == 'user':
                self.username = eachline[1]
            elif eachline[0] == 'pass':
                self.password = eachline[1]
            elif eachline[0] == 'ip':
                self.ipaddress = eachline[1]
            elif eachline[0] == 'port':
                self.port = eachline[1]
            elif eachline[0] == 'dbname':
                self.dbname = eachline[1]
            elif eachline[0] == 'charset':
                self.charset = eachline[1]
            elif eachline[0] == 'tableproject':
                self.project = eachline[1]

    def ProjectSearch(self):
        
        amtlist = []
        
#        createcmd = "%s://%s:%s@%s:%s/%s?charset=%s" % (self.dbtype, self.username, self.password, self.ipaddress, self.port, self.dbname, self.charset)
#        searchcmd = "select * from %s" % self.project
#
#        engine =  create_engine(createcmd, echo=True)
#        connection = engine.connect()
#        result = connection.execute(searchcmd)
        import os
        os.environ['TDSVER'] = '8.0'
        
        searchcmd = "select * from %s" % self.project
        
        connstring = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;PORT=%s;TDS_Version=8.0" % (self.dbtype, self.ipaddress, self.dbname, self.username, self.password, self.port)
        link = pyodbc.connect(connstring)
        cursor = link.cursor()
        cursor.execute(searchcmd)
        result = cursor.fetchall()
        
        for row in result:
            tmpDict = {}
            tmpDict['ProjectID'] = row[0]
            
            tmpgamePYname = row[1]
            if type(tmpgamePYname).__name__ == 'str':
                tmpgamePYname = tmpgamePYname.decode('gbk','ignore')
                tmpgamePYname = tmpgamePYname.encode('utf8')
            else:
                tmpgamePYname = tmpgamePYname.encode('utf8')
            tmpDict['gamePYname'] = tmpgamePYname
            
            tmpDict['gamename'] = row[2]
            amtlist.append(tmpDict)

        
        cursor.close()
        link.close()
        
        return amtlist