# -*- coding: utf-8 -*-
''' @author : majian'''

import time, os, re, sys
import simplejson as json

from BaseClass.verifityDependence import changeList, changeDict

class eventContent:
    
    def __init__(self):
        
        self.oc = ""
        self.smcd = ""
        self.mail = {}
        self.Content = {}
                
    def changeContent(self, templatetype, ipaddress, content):
         
        ''' Process Inform Part '''
        tmpdict = []
        if templatetype == 'processInform':
            if len(content) > 0:
                tmpdict = []
                for key,value in content.items():
                    if value > 0:
                        lack = "[%s](%s) : 缺少 %s个." % (ipaddress, key, value)
                        tmpdict.append(lack)
                    elif value < 0:
                        more = "[%s](%s) : 超过%s个." % (ipaddress, key, abs(value))
                        tmpdict.append(more)
            else:
                tmpdict = 'None' 
        
        if tmpdict != 'None':        
            self.oc = tmpdict
            self.smcd = tmpdict
            self.mail['subject'] = 'processInform'
            self.mail['content'] = tmpdict
            content = dict(oc=self.oc, smcd=self.smcd, mail=self.mail)
            contents = changeDict().dicttostr(content)
        else:
            self.oc = 'None'
            self.smcd = 'None'
            self.mail['subject'] = 'processInform'
            self.mail['content'] = 'None'
            content = dict(oc=self.oc, smcd=self.smcd, mail=self.mail)
            contents = changeDict().dicttostr(content)
                 
        return dict(Status='Success', content=contents)   