# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

class ReadCurves:
    
    def __init__(self):
        
        self.returns = ""
        
    ''' Curves of number explain '''    
    def changeReadlist(self, list):
        
        newList = []
        
        for eachVar in range(len(list)):
            if list[eachVar] == 0:
                tmpresult = '%s minutes: %s' % (int(eachVar)+1, 'nochange')
                newList.append(tmpresult)
            elif list[eachVar] > 0:
                tmpresult = '%s minutes: UP %s people' % (int(eachVar)+1, list[eachVar])
                newList.append(tmpresult)
            elif list[eachVar] < 0:
                tmpresult = '%s minutes: LOSE %s people' % (int(eachVar)+1, list[eachVar])
                newList.append(tmpresult)
                
        return newList
                