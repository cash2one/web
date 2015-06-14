# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import urllib2
import chardet

from ServiceConfig.config import readFromConfigFile

class urloperation:
    
    def __init__(self):
        
        self.url = ""
        
        getReturn = readFromConfigFile().get_config_zonedetailurl()
        for eachline in getReturn['ZoneDetailUrl']:
            if eachline[0] == 'url':
                self.url = eachline[1]
                
    def analystplatformzonedetail(self):
        
        alllist = []
        urlnew = urllib2.urlopen(self.url)

        if urlnew.getcode() == 200:
            for eachurlline in urlnew.readlines():
                if type(eachurlline).__name__ == 'str':
                    eachurlline = eachurlline.decode('gb2312','ignore')
                    eachurlline = eachurlline.encode('utf8')
                else:
                    eachurlline = eachurlline.encode('utf8')

                tmpDict = {}    
                tmpDict['gamePYname'] = re.split(',', eachurlline)[0]
                tmpDict['zonePYname'] = re.split(',', eachurlline)[1]
                tmpDict['zonename'] = re.split(',', eachurlline)[2]
                alllist.append(tmpDict)
                
            return dict(Status='Success', list=alllist)
                
        else:
            urlnew.close()    
            return dict(Status='False', msg='Could not found ')  
