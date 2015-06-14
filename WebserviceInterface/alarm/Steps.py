# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import pdb

from BaseClass.verifityDependence import changeDict
from alarmScheduler import Scheduler

class BasicStep:
    
    def __init__(self):
        
        self.returns = ""
        
    def judgeVariable(self, message):
        
        tmpcount = 0
        
        if type(message).__name__ == 'dict':
            for key,value in message.items():
                if key == 'Project':
                    tmpcount += 1
                elif key == 'Eventlevel':
                    tmpcount += 1
                elif key == 'Mbody':
                    tmpcount += 1
                elif key == 'Timestamp':
                    tmpcount += 1
                    
        else:
            return dict(Status='False', msg='Input message body format UNRIGHT.')
        
        if tmpcount == 5:
            return dict(Status='Success')
        else:
            return dict(Status='False', msg='Input message count not fit Variable.')
        
    def basicFilling(self, message):
        
        tmpBasicFilling = 0
        
        try:
            for key,value in message.items():
            
                if key == 'Project':
                    if value == '' or value == 'None':
                        return dict(Status='False', msg='Project could not be None.')
                    elif len(value) > 20 :
                        return dict(Status='False', msg='Project input length over 20. ERROR.')
                
                elif key == 'Eventlevel':
                    if value == '' or value == 'None':
                        message['Eventlevel'] = -1
                    elif int(value) > 10:
                        return dict(Status='False', msg='EventLevel uncorrect.')

                elif key == 'Mbody':
                    if type(value).__name__ == 'dict':
                        if type(value['oc']).__name__ != 'str':
                            return dict(Status='False', msg='Mbody-oc format not correct.')
                        elif type(value['smcd']).__name__ != 'str':
                            return dict(Status='False', msg='Mbody-smcd format not correct.')
                        elif type(value['mail']).__name__ != 'dict':
                            return dict(Status='False', msg='Mbody-mail format not correct.')
                    elif type(value).__name__ == 'str':
                        
                        value = changeDict().strtodict(value)
                        
                        if type(value['oc']).__name__ == 'str' or type(value['oc']).__name__ == 'unicode':
                            tmpBasicFilling += 1
                        else:
                            return dict(Status='False', msg='Mbody-oc format not correct.')
                        
                        if type(value['smcd']).__name__ == 'str' or type(value['smcd']).__name__ == 'unicode':
                            tmpBasicFilling += 1
                        else:    
                            return dict(Status='False', msg='Mbody-smcd format not correct.')
                        
                        if type(value['mail']).__name__ != 'dict':
                            return dict(Status='False', msg='Mbody-mail format not correct.')
                    else:
                        return dict(Status='False', msg='Mbody format not correct.')
                
                elif key == 'Timestamp':
                    if value == '' or value == 'None':
                        message['Timestamp'] = 0   
                    elif len(str(value)) != 10:
                        return dict(Status='False', msg='Timestamp length ERROR.')

        except Exception, e:
            return str(e)
        
        return dict(Status='Success', message=message)
    
    def decideEvent(self, eventgrade, message):
        
        print "##### eventgrade, message:", eventgrade, message
        if type(message).__name__ == 'str':
            message = changeDict().strtodict(message)
        
        ''' 
        Get Event Grade in table.eventgraderelation 
        example : {'Status': 'Success', 'mail': 0L, 'oc': 1L, 'smcd': 0L}
        '''
        getReturnofgrade = Scheduler().geteventgraderelation(eventgrade)
        if getReturnofgrade['Status'] != 'Success':
            return getReturnofgrade
        
        for key,value in message.items():
            if key == 'oc':
                if getReturnofgrade['oc'] == 1:
                    try:
                        if value == '':
                            print 'oc: get Variable ok'
                    except NameError:
                        return dict(Status=False, msg='oc: Value NameError.')
                                        
            elif key == 'mail':
                if getReturnofgrade['mail'] == 1:
                    try:
                        if value == '':
                            print 'mail: get Variable ok'
                    except NameError:
                        return dict(Status=False, msg='mail: Value NameError.')
                    
            elif key == 'smcd':
                if getReturnofgrade['smcd'] == 1:
                    try:
                        if value == '':
                            return dict(Status=False, msg='smcd: Value must exist. Not Null.')
                    except NameError:
                        return dict(Status=False, msg='smcd: Value NameError.')               
        
        return dict(Status='Success')            
        
        
    def judgeVariablebyoid(self, message):
        
        tmpcount = 0
        
        if type(message).__name__ == 'dict':
            for key,value in message.items():
                if key == 'Project':
                    tmpcount += 1
                elif key == 'Eventlevel':
                    tmpcount += 1
                elif key == 'Mbody':
                    tmpcount += 1
                elif key == 'Timestamp':
                    tmpcount += 1
                elif key == 'Oid':
                    tmpcount += 1
                    
        else:
            return dict(Status='False', msg='Input message body format UNRIGHT.')
        
        if tmpcount == 5:
            return dict(Status='Success')
        else:
            return dict(Status='False', msg='Input message count not fit Variable.')
        
    def basicFillingbyoid(self, message):
        
        tmpBasicFilling = 0
        
        try:
            for key,value in message.items():
            
                if key == 'Project':
                    if value == '' or value == 'None':
                        return dict(Status='False', msg='Project could not be None.')
                    elif len(value) > 20 :
                        return dict(Status='False', msg='Project input length over 20. ERROR.')
                
                elif key == 'Eventlevel':
                    if value == '' or value == 'None':
                        message['Eventlevel'] = -1
                    elif int(value) > 10:
                        return dict(Status='False', msg='EventLevel uncorrect.')

                elif key == 'Mbody':
                    if type(value).__name__ == 'dict':
                        if type(value['oc']).__name__ != 'str':
                            return dict(Status='False', msg='Mbody-oc format not correct.')
                        elif type(value['smcd']).__name__ != 'str':
                            return dict(Status='False', msg='Mbody-smcd format not correct.')
                        elif type(value['mail']).__name__ != 'dict':
                            return dict(Status='False', msg='Mbody-mail format not correct.')
                    elif type(value).__name__ == 'str':
                        
                        value = changeDict().strtodict(value)
                        
                        if type(value['oc']).__name__ == 'str' or type(value['oc']).__name__ == 'unicode':
                            tmpBasicFilling += 1
                        else:
                            return dict(Status='False', msg='Mbody-oc format not correct.')
                        
                        if type(value['smcd']).__name__ == 'str' or type(value['smcd']).__name__ == 'unicode':
                            tmpBasicFilling += 1
                        else:    
                            return dict(Status='False', msg='Mbody-smcd format not correct.')
                        
                        if type(value['mail']).__name__ != 'dict':
                            return dict(Status='False', msg='Mbody-mail format not correct.')
                    else:
                        return dict(Status='False', msg='Mbody format not correct.')
                
                elif key == 'Timestamp':
                    if value == '' or value == 'None':
                        message['Timestamp'] = 0   
                    elif len(str(value)) != 10:
                        return dict(Status='False', msg='Timestamp length ERROR.')
                    
                elif key == 'Oid':
                    if value == '' or value == 'None':
                        message['Oid'] = 'None'
                     
        except Exception, e:
            return str(e)
        
        return dict(Status='Success', message=message)