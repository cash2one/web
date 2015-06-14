# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import urllib2
import chardet

from ServiceConfig.config import readFromConfigFile
from urllib2 import URLError

class SMCDinterface:
    
    def __init__(self):
        
        self.host = ""
        self.port = ""
        self.method = ""
        self.gametype = ""
        self.acttype = ""
        self.getReturn = {}
      
        configAnalyst = readFromConfigFile().get_config_SMCDServer('/WebserviceInterface/ServiceConfig/setting.ini')
        
        for key,value in configAnalyst.items():
            if key == 'SMCDServer':
                for eachValue in range(len(value)):
                    if value[eachValue][0] == 'host':
                        self.host = value[eachValue][1]
                    elif value[eachValue][0] == 'port':
                        self.port = value[eachValue][1]
                    elif value[eachValue][0] == 'method':
                        self.method = value[eachValue][1]
                    elif value[eachValue][0] == 'acttype':
                        self.acttype = value[eachValue][1]
                    elif value[eachValue][0] == 'gametype':
                        self.gametype = value[eachValue][1]
                        
    def sendingMessage(self, dest_mobile='None', msg_content='None', sender='100000', priority=1, serverid=100000):
        
        #msg_content_mid = msg_content.decode()
        if type(msg_content).__name__ == 'str':
            msg_content = msg_content.decode("unicode-escape")
            msg_content = msg_content.encode('gb2312')
            msg_content = urllib2.quote(msg_content)
        else:
            msg_content = msg_content.encode('gb2312')
            msg_content = urllib2.quote(msg_content)
            
        url = 'http://%s:%s/%s?dest_mobile=%s&msg_content=%s&sender=%s&priority=%s&serverid=%s&gametype=%s&acttype=%s' % (self.host, self.port, self.method, dest_mobile, msg_content, sender, priority, serverid, self.gametype, self.acttype)
        if dest_mobile != 'None' and msg_content != 'None' and sender != 'None':
            if re.search(r'\d{11}', dest_mobile) and re.search(r'\d{5}', sender):
                try:
                    response = urllib2.urlopen(url)
                    return dict(Status='Success', dest_mobile=dest_mobile, sender=sender)
            
                except URLError, e:
                    return dict(Status='False', msg='Urlopen Error, code: 404')
            else:
                return dict(Status='False', msg='Method variable not correct.')
        else:
            return dict(Status='False', msg='Method variable not Complete.')
