# -*- coding: utf-8 -*-
''' @author : majian'''

import os, re, sys
import time

class AlarmExplain:
    
    def __init__(self):
        
        self.returns = ""
        
    def getExplainofNumberofCurves(self, data):
        
        newReturn = {}
        
	print "############ eachData:", data
	
	try:
            for eachValue in data:
                if eachValue != '':
    		    print "########### eachValue:", eachValue
                    for key,value in eachValue.items():
                        if key == 'LosePeople':
                            newReturn['ActuallyHold'] = eachValue['Standard']
                            newReturn['ActuallyLose'] = eachValue['Actual']
                            newReturn['Time'] = eachValue['TimeOccur']
                            
                        elif key == 'LosePercent':
                            newReturn['PercentHold'] = eachValue['Standard']
                            newReturn['PercentActually'] = eachValue['Actual']
                            newReturn['Time'] = eachValue['TimeOccur']
                            
    		        elif key == 'Status':
			    for secondKey, secondValue in eachValue.items():
				if secondKey == 'holdpercent':
				    newReturn['Wholepercenthold'] = secondValue
				elif secondKey == 'actualpercent':
				    newReturn['Wholepercentactually'] = secondValue
				elif secondKey == 'holdpeople':
				    newReturn['Wholepeoplehold'] = secondValue
				elif secondKey == 'actualpeople':
				    newReturn['Wholepeopleactually'] = secondValue
     
    			    newReturn['Time'] = eachValue['Time']
    
	except Exception, e:
	    return e

        return newReturn
