# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

class HumanRead:
    
    def __init__(self):
        
        self.returns = ""
        
    def ReadtoHuman(self, OIDname, ComputerLanguage):
        
	'''
	Situation 1. whole game 
	{'ZTII': {'ReturnValue': {'percent': {'Status': 'Over', 'hold': '2', 'actual': 3}}}}
	
	Situation 2. single area
        {u'ZTQY': u'Could not found ONLINENUM20130306', 
	 u'SGZH': {
			u'\u53cc\u7ebf1\u533a(\u53cc\u7ebf)': [0, 1000, 1000, 3000], 
			u'\u53cc\u7ebf2\u533a': [0, -2000, 1000, 1000]
		  }
	}
	'''
        
        newHumanRead = {}
        
        ''' This part is used to number of curves '''
        if OIDname == 'numberofcurves':
            
            for key,value in ComputerLanguage.items():
                if type(value).__name__ == 'str' or type(value).__name__ == 'unicode':
                    newHumanRead[key] = 'can not get number of curves from platform , perhaps %s not exist.' % re.split('Could not found ',value)[1]
     
                elif type(value).__name__ == 'dict':
                    tmpDict = {}
                    for k,v in value.items():
                        
                        if type(v).__name__ == 'list':

                            tmpCount = []
                            for eachV in v:
                                
                                for vkey,vvalue in eachV.items():
                                    if vkey == 'LosePeople':
                                        if vvalue == 'Over':
                                            tmpCount.append(eachV)
                                    if vkey == 'LosePercent':
                                        if vvalue == 'Over':
                                            tmpCount.append(eachV)
                                          
                                tmpDict[k] = tmpCount

			elif k == 'ReturnValue':
			    # v : {'percent': {'Status': 'Over', 'hold': '2', 'actual': 3}}
			    for eachK, eachV in v.items():
			    	tmpDict[eachK] = eachV	
                
                    newHumanRead[key] = tmpDict
                    
        return newHumanRead
            
