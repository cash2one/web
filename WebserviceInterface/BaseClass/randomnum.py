# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time
import random

class RandomNum:
    
    def getRandom(self, pos):
        
        i = 0
        j = 0
        getnum = 0
        
        if type(pos).__name__ != 'int':
            return dict(Status='False', msg='input pos type not right.')
        
        if pos == 1:
            getnum = random.randint(1,9)
            
        elif pos > 1:
            count = int(pos - 1)
            
            beforeint = "1"
            afterint = "9"
            
            for i in range(count):
                beforeint += "0"
            
            for j in range(count):
                afterint += "9"
                
            getnum = random.randint(int(beforeint), int(afterint))
            
        elif pos <= 0:
            return dict(Status='False', msg='input pos not right.')
        
        return dict(Status='Success', randomnum=getnum)