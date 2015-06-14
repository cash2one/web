# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from interface.lync import Alarm
from interface.mail import SendMail
from interface.smcd import SMCDinterface
import simplejson as json

class BroadcastMain:
    
    def __init__(self):
        
        self.returns = ""
        
        ''' 
        Input Data example:
        data : dict 
        userDict : dict : 'Status': 'Success'
        '''
    def Control(self, data, userDict):
        
        ''' Delete userDict['Status'] '''
        if userDict['Status']:
            del userDict['Status']
        
        ''' search each people '''
        for personName, informDict in userDict.items():

            for method, value in informDict.items():
                #''' OC interface '''
                if method == 'OC':
                    if value or value != '':
                        for ResultSeq, Result in data.items():
                            
                            ''' change output format to string and 4 lines '''
                            if type(Result).__name__ != 'str':
                                newData = "\r".join(Result)
                            else:
                                newData = Result

                            print "######## newData:", newData
                            Alarm().officeCommunicate('majian@ztgame.com', value, newData, 'http://www.baidu.com')
                
                #''' Shoft message interface '''            
                elif method == 'SMCD':
                    if value or value != '':
                         for ResultSeq, Result in data.items():
                            
                            ''' change output format to string and 4 lines '''
                            if type(Result).__name__ != 'str':
                                newData = "||".join(Result)
                            else:
                                newData = Result
                                
                            SMCDinterface().sendingMessage(value, newData, '13091', 1, 100000)
#                
#                #''' Mail interface '''         
#                elif method == 'Mail':
#                    if value or value != '':  
#                        for ResultSeq, Result in data.items():
#                            
#                            ''' change output format to string and 4 lines '''
#                            if type(Result).__name__ != 'str':
#                                newData = "\r".join(Result)
#                            else:
#                                newData = Result
#                                
#                            SendMail().send_mail('majian@ztgame.com', value, 'numberofcurves', newData) 