# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from BaseClass.verifityDependence import changeDict
from BaseClass.grade import Warning

class Event:
    
    def __init__(self):
        
        self.returns = ""
        
    def Control(self, oid, Var, varGET, data, useMethod):
        
        ''' Basic data handle '''
        tmplist = []
        tmplist = re.split(',', varGET)
        
        data = changeDict().strtodict(data)  
        
        ''' choose each Method with Simple Use '''
        
        ''' noneed part : 
        this method used by no need any methods just compare with varGET 
        *** use thres to judge this is an abnormal ***
        '''
        if useMethod == 'noneed':
        
            for key,value in data.items():
                softlimit = tmplist[1]
                hardlimit = tmplist[2]
                if key == Var:
                    if int(value) < int(softlimit):
                        getWarningTransport = Warning().grade(0)
                    elif int(softlimit) < int(value) < int(hardlimit):
                        getWarningTransport = Warning().grade(1)
                    elif int(value) > int(hardlimit):
                        getWarningTransport = Warning().grade(-1)
                        
                    return getWarningTransport
                    
                        
        else:
            return dict(Status='False', msg='could not found right method.')