# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re
import sys

class percentCalc:
    
    def __init__(self):
        
        self.returns = ""
        
    ''' 
    percent calcuation  
    example :  100/200 -> keep A rounded for result
    '''    
    def percent(self, divisor, dvidend):
        
        Result = float(divisor) / float(dvidend)
        
        perResult = round(Result * 100, 0)
        
        perFinish = str(int(perResult))+"%"
        
        return perFinish
        
        
        