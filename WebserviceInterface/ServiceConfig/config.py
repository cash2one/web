# -*- coding: utf-8 -*-
''' @author : majian'''

import re, os, sys, traceback
import ConfigParser

class readFromConfigFile:
    ''' This is read from setttings.ini '''

    def __init__(self,sqlalchemy='splite:///:memory:'):
        self.itemsResult = {}
        self.oracleResult = {}
        self.mysqlResult = {}
        self.curvesResult = {}
        self.lync = {}
        self.zonelist = {}
        self.smsinform = {}
        self.tableRelationDict = {}
        self.thresholdDict = {}
        self.threscalc = {}
        self.Alarm = {}
        self.sqlalchemy = sqlalchemy
        
    def get_config_giantAMT(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()
        
        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'AMT':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['AMT'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
        
    def get_config_giantauto(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()
        
        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'GiantAuto':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['GiantAuto'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
        
    def get_config_zonedetailurl(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()
        
        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'ZoneDetailUrl':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['ZoneDetailUrl'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()

    def get_config_xinetd(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()
        
        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Xinetd':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['Xinetd'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
            
    def get_config_Log(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()
        
        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Log':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['Log'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()

    def get_config_sqlalchemy(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):

        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'database':
                        options = statement.options(eachSection)
                        if options:
                            self.itemsResult['database'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                    elif eachSection == 'interfaceDB':
                        options = statement.options(eachSection)
                        self.itemsResult['interfaceDB'] = statement.items(eachSection)
                    elif eachSection == 'windowsAD':
                        options = statement.options(eachSection)
                        self.itemsResult['windowsAD'] = statement.items(eachSection)
                    elif eachSection == 'ConfigManagerDB':
                        options = statement.options(eachSection)
                        self.itemsResult['ConfigManagerDB'] = statement.items(eachSection)
                        
                return self.itemsResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
            
    def get_config_oracle(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Oracle':
                        options = statement.options(eachSection)
                        if options:
                            self.oracleResult['Oracle'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                        
                return self.oracleResult
            
            else:
                return "%s hasn't any oracle information" % filePath

        except Exception, e:
            traceback.print_exc()
            
    def get_config_mysql(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'database':
                        options = statement.options(eachSection)
                        if options:
                            self.mysqlResult['database'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                    elif eachSection == 'interfaceDB':
                        options = statement.options(eachSection)
                        self.mysqlResult['interfaceDB'] = statement.items(eachSection)
     
                        
                return self.mysqlResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
         
    def get_config_mainserver(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'MainServer':
                        options = statement.options(eachSection)
                        if options:
                            self.mysqlResult['MainServer'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.mysqlResult
            
            else:
                return "%s hasn't any default information" % filePath

        except Exception, e:
            traceback.print_exc()
            
    def get_config_curves(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'CurvesUrl':
                        options = statement.options(eachSection)
                        if options:
                            self.curvesResult['CurvesUrl'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.curvesResult
            
        except Exception, e:
            traceback.print_exc()
            
    def get_config_lync(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Lync':
                        options = statement.options(eachSection)
                        if options:
                            self.lync['Lync'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.lync
            
        except Exception, e:
            traceback.print_exc()    
            
    def get_config_zonelist(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Zonelist':
                        options = statement.options(eachSection)
                        if options:
                            self.zonelist['Zonelist'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.zonelist
            
        except Exception, e:
            traceback.print_exc()    
            
    def get_config_SMCDServer(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'SMCDServer':
                        options = statement.options(eachSection)
                        if options:
                            self.smsinform['SMCDServer'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.smsinform
            
        except Exception, e:
            traceback.print_exc()
            
    def get_config_tableRelation(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'tableRelation':
                        options = statement.options(eachSection)
                        if options:
                            self.tableRelationDict['tableRelation'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.tableRelationDict
            
        except Exception, e:
            traceback.print_exc()
            
    def get_config_ThresHold(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'ThresHold':
                        options = statement.options(eachSection)
                        if options:
                            self.thresholdDict['ThresHold'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.thresholdDict
            
        except Exception, e:
            traceback.print_exc()
            
    def get_config_thresCalculation(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'thresCalculation':
                        options = statement.options(eachSection)
                        if options:
                            self.threscalc['thresCalculation'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.threscalc
            
        except Exception, e:
            traceback.print_exc()
            
    def get_config_Alarm(self, filePath='/WebserviceInterface/ServiceConfig/setting.ini'):
        
        statement = ConfigParser.ConfigParser()  
        statement.read(filePath)
        sections = statement.sections()

        try:
            if sections:
                for eachSection in sections:
                    if eachSection == 'Alarm':
                        options = statement.options(eachSection)
                        if options:
                            self.Alarm['Alarm'] = statement.items(eachSection)
                        else:
                            return "%s hasn't any key/values" % eachSection
                           
                return self.Alarm
            
        except Exception, e:
            traceback.print_exc()
