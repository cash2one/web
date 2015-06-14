# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import urllib2
from config import readFromConfigFile

class Urlex:
    
    def __init__(self):
        
        # get URL from config file
        # self.url store all url information
        self.url = ""
        self.getResult = {}
        
        analystConfig = readFromConfigFile()
        getAnalyst = analystConfig.get_config_curves('/WebserviceInterface/ServiceConfig/setting.ini')  
        for key,value in getAnalyst.items():
            if key == 'CurvesUrl':
                for eachValue in value:
                    if eachValue[0] == 'url':
                        self.url = eachValue[1]
        
        self.getResponse = urllib2.urlopen(self.url).readlines()
     
    # Thid Method used to select url about infoserver : host, port, username, password
    # and make it into dict return   
    def getInformationSingle(self, variable):
        
        count = 0
        for eachResponse in self.getResponse:
            if re.search(r'InfoServerDB', eachResponse):
                partb=re.split(r'\ DB=\"',eachResponse)[1]
                name = re.split(r'\"',partb)[0]
                if re.search(variable.upper(), eachResponse.upper()):
                    count += 1
                    part=re.split(r'InfoServerDB Server=\"',eachResponse)[1]
                    ipaddress = re.split(r'\"',part)[0]
                    if re.search('\_',name):
                        game = re.split("\_",name)[1]
                    else:
                        game = 'NULL'
                    partc=re.split(r'\ User=\"',eachResponse)[1]
                    username = re.split(r'\"',partc)[0]
                    partd=re.split(r'\ Password=\"',eachResponse)[1]
                    password = re.split(r'\"',partd)[0]
                    parte=re.split(r'\ Port=\"',eachResponse)[1]
                    port=re.split(r'\"',parte)[0]
                    self.getResult[game]=dict(ipaddress=ipaddress, port=int(port), username=username, password=password, dbname=name) 
                    
        if count == 0:
            msg = 'Get Variable ERROR.'
            return msg

        return self.getResult
    
    def getInformationMultiple(self, variable):
        
        try:
            for eachResponse in self.getResponse:
                if re.search(r'InfoServerDB', eachResponse):  
                    part=re.split(r'InfoServerDB Server=\"',eachResponse)[1]
                    ipaddress = re.split(r'\"',part)[0]
                    partb=re.split(r'\ DB=\"',eachResponse)[1]
                    name = re.split(r'\"',partb)[0]
                    if re.search('\_',name):
                        game = re.split("\_",name)[1]
                    else:
                        game = 'NULL'
                    partc=re.split(r'\ User=\"',eachResponse)[1]
                    username = re.split(r'\"',partc)[0]
                    partd=re.split(r'\ Password=\"',eachResponse)[1]
                    password = re.split(r'\"',partd)[0]
                    parte=re.split(r'\ Port=\"',eachResponse)[1]
                    port=re.split(r'\"',parte)[0] 
                    
                    self.getResult[game]=dict(ipaddress=ipaddress, port=int(port), username=username, password=password, dbname=name)
                    
        except Exception, e:
            return e
        
        return self.getResult
