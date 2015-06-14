# -*- coding: utf-8 -*-
''' @author : majian'''

import time, os
import sys, re

from BaseClass.verifityDependence import changeDict
from interface.lync import Alarm
from interface.smcd import SMCDinterface
from interface.mail import SendMail

class Manager:
    
    def __init__(self):
        
        self.returns = ""
    
    ''' 
    This method Control all broadcast for User
    input example : 
    userDict: dict:  {'feijun': {'MAIL': 'feijun@ztgame.com', 'OC': 'feijun@ztgame.com', 'SMCD': '18616193305'}}
    informDict: str: {u'mail': {u'content': u'this is mail message', u'subject': u'mail subject'}, u'oc': u'this is oc message', u'smcd': u'this is smcd message'}
    '''
        
    def Main(self, userDict, informDict):

        if type(informDict).__name__ != 'dict':
            informDict = changeDict().strtodict(informDict)
        
        for userKey, userValue in userDict.items():
            for eachMethod, eachValue in userValue.items():
                if eachMethod == 'OC':
                    if eachValue:
                        Alarm().officeCommunicate('8000@ztgame.com', eachValue, informDict[eachMethod.lower()])
                    elif eachValue == '':
                        print "user: %s, oc: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')
                        
                elif eachMethod == 'SMCD':
                    if eachValue:
                        SMCDinterface().sendingMessage(eachValue, informDict[eachMethod.lower()])
                    elif eachValue == '':
                        print "user: %s, smcd: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')
                        
#                elif eachMethod == 'MAIL':
#                    if eachValue:
#                        if len(informDict[eachMethod.lower()]['subject']) != 0:
#                            SendMail().send_mail('8000@ztgame.com', eachValue, informDict[eachMethod.lower()]['subject'], informDict[eachMethod.lower()]['content'])
#                    elif eachValue == '':
#                        print "user: %s, mail: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')  
                        
        return dict(Status='Success')
                        
    def TestBroadcastMain(self, userDict, informDict):

        if type(informDict).__name__ != 'dict':
            informDict = changeDict().strtodict(informDict)
        
        for userKey, userValue in userDict.items():
            for eachMethod, eachValue in userValue.items():
                if eachMethod == 'OC':
                    if eachValue:
                        print "user: %s, oc: %s, information: %s, type: %s" % (userKey, eachValue, informDict[eachMethod.lower()], type(informDict[eachMethod.lower()]))
                    elif eachValue == '':
                        print "user: %s, oc: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')
                        
                elif eachMethod == 'SMCD':
                    if eachValue:
                        print "user: %s, smcd: %s, information: %s, type: %s" % (userKey, eachValue, informDict[eachMethod.lower()], type(informDict[eachMethod.lower()]))
                    elif eachValue == '':
                        print "user: %s, smcd: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')
                        
                elif eachMethod == 'MAIL':
                    if eachValue:
                        print "user: %s, mail: %s, information: %s, type: %s" % (userKey, eachValue, informDict[eachMethod.lower()], type(informDict[eachMethod.lower()]))
                    elif eachValue == '':
                        print "user: %s, mail: %s, information: %s, type: %s" % (userKey, eachValue, 'oc information is NULL')
                        
        return dict(Status='Success')