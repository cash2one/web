# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

from BaseClass.verifityDependence import changeDict
from event.Base.eventDepend import Depend

class EventCalc:
    
    def __init__(self):
        
        self.returns = ""
        
    def CalcControl(self, OIDname, Result):
        
        newResult = ""
        reback = {}
        
        ''' the Curves of people '''
        if OIDname == 'numberofcurves':
            if type(Result).__name__ == 'str':
                newResult = changeDict().strtodict(Result)
            elif type(Result).__name__ == 'dict':
                newResult = Result
            else:
                return 'get %s of Input ERROR.' % OIDname
            
            ''' Part of game '''
            for key,value in newResult.items():
                ''' value: {u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [22222, 22222, 23222, 24222, 27222], u'\u53cc\u7ebf2\u533a': [11111, 11111, 9111, 10111, 11111]}'''
                if type(value).__name__ == 'str' or type(value).__name__ == 'unicode':
                    reback[key] = value
                    
                elif type(value).__name__ == 'dict':
                    getCalcResult = Depend().CurvesManage(value)
                    reback[key] = getCalcResult
                    
            return reback