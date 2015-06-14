# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

''' This method is used by Event grade judge '''
class Event:
    
    def __init__(self):
        
        self.returns = ""

    '''
    Grade :
    5: level 5 event  
    4: level 4 event
    3: level 3 event
    2: level 2 event
    1: level 1 event
    0: not event
    '''        
    def judge(self, singal):
        
        if type(singal).__name__ == 'int':
            
            if singal > 5 or singal < 0:
                return self.error()
            else:
                return self.right()
            
        else:
            return self.error()
    
    ''' error message '''    
    def error(self):
        
        return False
    
    ''' right message '''
    def right(self):
        
        return True

''' This method used by warning '''            
class Warning:
    
    def __init__(self):
        
        self.returns = ""
        
    ''' 
    used to judge singal is already fix the claim
    '''
    def judge(self, singal):
        
        if type(singal).__name__ == 'int':
            
            if singal > -2 and singal < 2:
                return self.right()
            else:
                return self.error()               
            
        else:
            return self.error()
    '''
    0 : currect abnormal : True(boolean)
    1 : warning abnormal : Warning(string)
    -1 : error abnormal : False(boolean)
    '''   
    def grade(self, singal):
        
        if self.judge(singal) == True:
            if singal == 0:
                return True
            elif singal == 1:
                return 'Warning'
            elif singal == -1:
                return False
        else:
            return self.judge(singal)
        
    ''' error message '''        
    def error(self):
        
        return False
    
    ''' right message '''
    def right(self):
        
        return True
