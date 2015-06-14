# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import cx_Oracle, MySQLdb

from ServiceConfig.config import readFromConfigFile
from model.asset import ASSET
from model import metadata, DBSession, declarativeBase

class getAllserver:
    
    def __init__(self):
        
        # All Search Result
        self.all = ''
        self.cursor = ''        # oracle used cursor
        self.OracleConn = ''
       
        # Statement about oracle
        self.LANG, self.orclname, self.orclpass, self.orcldb, self.orclhost, self.orclport = '','','','','',''
        
        # Statement about mysql
        self.mysqluser, self.mysqlpass, self.mysqlhost, self.mysqlport, self.mysqldb = '','','','',''
        
        # Server Device information
        self.coreCount, self.coreModel, self.memCount, self.memCapacity, self.diskCount, self.diskCapacity='','','','','',''
        
        # get Oracle config file
        getConfigAnalyst = readFromConfigFile().get_config_oracle('/WebserviceInterface/ServiceConfig/setting.ini')
        
        for key,value in getConfigAnalyst.items():
            for eachele in range(len(value)):
                if value[eachele][0] == 'lang':
                    self.LANG = value[eachele][1]
                elif value[eachele][0] == 'username':
                    self.orclname = value[eachele][1]
                elif value[eachele][0] == 'password':
                    self.orclpass = value[eachele][1]
                elif value[eachele][0] == 'host':
                    self.orclhost = value[eachele][1]
                elif value[eachele][0] == 'port':
                    self.orclport = value[eachele][1]
                elif value[eachele][0] == 'dbname':
                    self.orcldb = value[eachele][1]
 
        # set client enviornment variable
        # oracle 将客户端的环境变量设置为 ZHS16GBK
        os.environ['NLS_LANG'] = self.LANG
        
        # new engine link with Oracle
        oracle_cmd = "%s/%s@%s:%s/%s" % (self.orclname, self.orclpass, self.orclhost, self.orclport, self.orcldb)
        self.OracleConn = cx_Oracle.connect(oracle_cmd)
        self.cursor = self.OracleConn.cursor()  
        
    def getDatabase(self):
    
        searchLocal = DBSession.query(ASSET).all()
        if len(searchLocal) > 100:
            print "local table.asset has data. needn't."
        else:
            self.flush(self.cursor)
            
        self.cursor.close()
        self.OracleConn.close()
        
    def Recovery(self):
        
        localAsset = DBSession.query(ASSET).all()

        if len(localAsset) > 100:
            for eachAsset in range(len(localAsset)):
                DBSession.delete(localAsset[eachAsset])
            DBSession.commit()
            
            self.flush(self.cursor)
        else:
            self.flush(self.cursor)
            
        self.cursor.close() 
        self.OracleConn.close()
    
    def flush(self, oracleCursor):
        
        # execute in oracle VIEW
        oracleCursor.execute('select * from MEP_ASSETREPORT')
        self.all = self.cursor.fetchall()
        
        for eachline in range(len(self.all)):
            DBSession.add(ASSET(eachline, self.all[eachline][1], self.all[eachline][2], self.all[eachline][3], self.all[eachline][4], self.all[eachline][5], self.all[eachline][6], self.all[eachline][7], self.all[eachline][8], self.all[eachline][9], self.all[eachline][10], self.all[eachline][11], self.all[eachline][13], self.all[eachline][14], self.all[eachline][15], self.all[eachline][17], self.all[eachline][22]))
        
        DBSession.commit()

# 中文字符集问题
# resultSet=engine.execute('select * from v$nls_parameters')
#   id               配置编号                               分类号                              资产编号                          使用属性                            核算项目                            主机名                                   内网                                    外网                                      存储网                                    使用人                                    机架位置                         zcbm                 使用人id            所属机房                            用途                                 是否使用中（Y/N）      
# self.all[eachline][0], self.all[eachline][1], self.all[eachline][2], self.all[eachline][3], self.all[eachline][4], self.all[eachline][5], self.all[eachline][6], self.all[eachline][7], self.all[eachline][8], self.all[eachline][9], self.all[eachline][10], self.all[eachline][11], self.all[eachline][13], self.all[eachline][14], self.all[eachline][15], self.all[eachline][17], self.all[eachline][22]
