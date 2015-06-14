# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from model.cmdbsearch import BasicSearch
from BaseClass.timeBasic import TimeBasic

class Expand:
    
    def __init__(self):
        
        self.returns = ""
        
    def checkadvariable(self, url, operation, starttime, overtime, project):
        
        count = 0
        
        # url check
        if type(url).__name__ != 'str':
            return dict(Status='False', msg='input url variable TYPE not correct.')
        else:
            if re.search(r'http://', url):
                count += 1
            else:
                return dict(Status='False', msg='Input url Variable is not right.')
    
        # operation check
        if type(operation).__name__ != 'str':
            return dict(Status='False', msg='input operation variable TYPE not correct.')
        else:
            if operation == 'add' or operation == 'del':
                count += 1
            else:
                return dict(Status='False', msg='Input operation Variable is not right.')
               
        # starttime check
        if len(str(starttime)) > 20:
            return dict(Status='False', msg='Input starttime Variable is not right.')
        else:
            count += 1
        
        # overtime check
        if len(str(overtime)) > 20:
            return dict(Status='False', msg='Input overtime Variable is not right.')
        else:
            count += 1
            
        if count == 4:
            return dict(Status='Success')
        else:
            return dict(Status='False', msg='Input Four Variable Error.')
    
    def checkaddordel(self, url, operation, starttime, overtime, project, pagealias):
        
        if operation == 'add':
            
            if re.search(r'\_', starttime):
                starttime = TimeBasic().timeADcontrol(starttime)
            
            if re.search(r'\_', overtime):
                overtime = TimeBasic().timeADcontrol(overtime)
                
            if starttime > overtime :
                return dict(Status='False', msg='input time Error. Overtime early than starttime.')
            else:
                return dict(Status='Success', url=url, operation=operation, starttime=starttime, overtime=overtime, project=project, pagealias=pagealias)    
            
        elif operation == 'del':
            
            if re.search(r'\_', starttime):
                starttime = TimeBasic().timeADcontrol(starttime)
            
            return dict(Status='Success', url=url, operation=operation, starttime=starttime, overtime=0, project=project, pagealias=pagealias)    
   
    def wholeUsingAction(self, url, operation, starttime, overtime, project, pagealias):
        
        # add new url check
        if operation == 'add':
            
            getaddandchange = BasicSearch().addintoadurl(url, starttime, overtime, 1, project, pagealias)
            return getaddandchange
            
        elif operation == 'del':
            
            getdel = BasicSearch().deladurl(url)
            return getdel
        